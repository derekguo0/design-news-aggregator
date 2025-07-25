"""
任务调度模块
实现定时执行爬取和推送任务
"""
import asyncio
from datetime import datetime, timezone
from typing import List, Callable, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from loguru import logger
import pytz

from ..config import get_config
from ..crawlers.base import create_crawler
from ..processors.content_processor import ContentProcessor
from ..generators.web_generator import WebGenerator
from ..services.statistics import StatisticsService
from ..models import NewsItem

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        self.config = get_config()
        self.scheduler = AsyncIOScheduler(timezone=pytz.timezone(self.config.scheduler.timezone))
        self.processor = ContentProcessor()
        self.web_generator = WebGenerator()
        self.stats_service = StatisticsService()
        self.is_running = False
        
        # 设置事件监听器
        self.scheduler.add_listener(self._job_executed, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self._job_error, EVENT_JOB_ERROR)
    
    def _job_executed(self, event):
        """任务执行成功回调"""
        logger.info(f"任务执行成功: {event.job_id}")
    
    def _job_error(self, event):
        """任务执行失败回调"""
        logger.error(f"任务执行失败: {event.job_id}, 异常: {event.exception}")
    
    async def crawl_all_sources(self) -> List[NewsItem]:
        """爬取所有资讯源"""
        logger.info("开始执行每日资讯爬取任务")
        
        all_items = []
        enabled_sources = [source for source in self.config.sources if source.enabled]
        
        logger.info(f"启用的资讯源数量: {len(enabled_sources)}")
        
        # 并发爬取所有资讯源
        crawl_tasks = []
        for source in enabled_sources:
            crawler = create_crawler(source)
            crawl_tasks.append(self._crawl_single_source(crawler))
        
        # 等待所有爬取任务完成
        results = await asyncio.gather(*crawl_tasks, return_exceptions=True)
        
        # 收集结果
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"爬取源 {enabled_sources[i].name} 失败: {result}")
            elif isinstance(result, list):
                all_items.extend(result)
                logger.info(f"爬取源 {enabled_sources[i].name} 成功: {len(result)} 条")
        
        logger.success(f"爬取任务完成，共获得 {len(all_items)} 条资讯")
        return all_items
    
    async def _crawl_single_source(self, crawler) -> List[NewsItem]:
        """爬取单个资讯源"""
        try:
            # 在新的线程中执行同步爬取操作
            loop = asyncio.get_event_loop()
            items = await loop.run_in_executor(None, crawler.crawl)
            return items
        except Exception as e:
            logger.error(f"爬取失败: {e}")
            return []
    
    async def daily_digest_task(self):
        """每日摘要任务"""
        try:
            logger.info("开始执行每日摘要任务")
            
            # 步骤1: 爬取所有资讯
            logger.info("步骤1: 爬取所有资讯...")
            items = await self.crawl_all_sources()
            
            if not items:
                logger.warning("没有获取到任何资讯，跳过报告生成")
                return
            
            logger.info(f"成功爬取 {len(items)} 条资讯")
            
            # 步骤2: 处理内容
            logger.info("步骤2: 处理内容...")
            processed_items = self.processor.process_items(items)
            
            if not processed_items:
                logger.warning("内容处理后没有有效资讯，跳过报告生成")
                return
                
            logger.info(f"成功处理 {len(processed_items)} 条有效资讯")
            
            # 步骤3: 生成每日摘要...
            logger.info("步骤3: 生成每日摘要...")
            daily_digest = self.processor.create_daily_digest(processed_items)
            
            # 步骤4: 生成网页
            logger.info("步骤4: 生成网页...")
            result = self.web_generator.generate_complete_site(daily_digest)
            
            if not result:
                logger.error("网页生成失败")
                return
                
            logger.success(f"网页生成成功: {result['output_dir']}")
            logger.info(f"首页: {result['index_page']}")
            logger.info(f"每日页面: {result['daily_page']}")
            logger.info(f"归档页面: {result['archive_page']}")
            
            # 步骤5: 生成统计报告
            logger.info("步骤5: 生成统计报告...")
            try:
                self.stats_service.save_statistics()
                
                # 简单统计
                basic_stats = self.stats_service.get_basic_statistics()
                logger.info(
                    f"📊 统计报告: 共处理 {basic_stats.get('total_articles', 0)} 条资讯"
                )
                          
            except Exception as e:
                logger.warning(f"统计报告生成失败: {e}")
            
            # 可以在这里添加部署逻辑
            # await self._deploy_to_github_pages(result['output_dir'])
                
        except KeyboardInterrupt:
            logger.info("用户中断任务执行")
            raise
        except Exception as e:
            logger.error(f"每日摘要任务执行失败: {e}")
            import traceback
            logger.debug(f"详细错误信息: {traceback.format_exc()}")
            raise
    
    async def _send_completion_notification(self, digest, site_url: str):
        """发送完成通知"""
        try:
            notification_content = f"""
📅 {digest.date.strftime('%Y年%m月%d日')} 设计资讯日报已生成
📊 共收集 {digest.total_items} 条资讯
🌐 来源网站 {len(digest.sources)} 个
🔗 查看网站: {site_url}
            """.strip()
            
            # 这里可以添加其他通知方式，比如邮件、Webhook等
            logger.info("完成通知已发送")
            
        except Exception as e:
            logger.error(f"发送完成通知失败: {e}")
    
    def add_daily_job(self):
        """添加每日任务"""
        trigger = CronTrigger(
            hour=self.config.scheduler.hour,
            minute=self.config.scheduler.minute,
            timezone=self.config.scheduler.timezone
        )
        
        self.scheduler.add_job(
            self.daily_digest_task,
            trigger=trigger,
            id="daily_digest",
            name="每日设计资讯摘要",
            replace_existing=True
        )
        
        logger.info(f"每日任务已添加: {self.config.scheduler.hour}:{self.config.scheduler.minute:02d}")
    
    def add_custom_job(self, func: Callable, trigger, job_id: str, name: str = None):
        """添加自定义任务"""
        self.scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            name=name or job_id,
            replace_existing=True
        )
        logger.info(f"自定义任务已添加: {job_id}")
    
    def remove_job(self, job_id: str):
        """移除任务"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"任务已移除: {job_id}")
        except Exception as e:
            logger.error(f"移除任务失败: {e}")
    
    def list_jobs(self):
        """列出所有任务"""
        jobs = self.scheduler.get_jobs()
        logger.info(f"当前任务数量: {len(jobs)}")
        
        for job in jobs:
            next_run = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else "N/A"
            logger.info(f"任务: {job.id} | 名称: {job.name} | 下次运行: {next_run}")
    
    def start(self):
        """启动调度器"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.success("任务调度器已启动")
        else:
            logger.warning("任务调度器已在运行中")
    
    def stop(self):
        """停止调度器"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("任务调度器已停止")
        else:
            logger.warning("任务调度器未在运行")
    
    async def run_once(self):
        """立即执行一次任务（用于测试）"""
        logger.info("立即执行一次每日摘要任务")
        await self.daily_digest_task()
    
    async def test_all_sources(self):
        """测试所有资讯源"""
        logger.info("开始测试所有资讯源")
        
        enabled_sources = [source for source in self.config.sources if source.enabled]
        
        for source in enabled_sources:
            try:
                logger.info(f"测试资讯源: {source.name}")
                crawler = create_crawler(source)
                items = await self._crawl_single_source(crawler)
                
                if items:
                    logger.success(f"✅ {source.name}: 成功获取 {len(items)} 条资讯")
                    # 显示第一条作为示例
                    if len(items) > 0:
                        first_item = items[0]
                        logger.info(f"   示例: {first_item.title}")
                else:
                    logger.warning(f"⚠️ {source.name}: 未获取到资讯")
                    
            except Exception as e:
                logger.error(f"❌ {source.name}: 测试失败 - {e}")
        
        logger.info("资讯源测试完成")
    
    async def test_web_generation(self):
        """测试网页生成功能"""
        logger.info("测试网页生成功能")
        
        try:
                        # 创建测试数据
            from datetime import datetime
            from ..models import NewsItem, DailyDigest, CategorySummary
            
            test_items = [
                NewsItem(
                    title="测试设计资讯1",
                    url="https://example.com/1",
                    author=None,
                    category="设计资讯",
                    source="测试源",
                    image_url=None,
                    summary="这是一条测试资讯的摘要内容",
                    tags=[],
                    stats=None,
                    published_at=None
                ),
                NewsItem(
                    title="测试设计资讯2", 
                    url="https://example.com/2",
                    author=None,
                    category="作品展示",
                    source="测试源",
                    image_url=None,
                    summary="这是另一条测试资讯的摘要内容",
                    tags=[],
                    stats=None,
                    published_at=None
                )
            ]
            
            test_digest = self.processor.create_daily_digest(test_items)
            
            # 测试生成网页
            result = self.web_generator.generate_complete_site(test_digest)
            
            if result:
                logger.success("✅ 网页生成功能正常")
                logger.info(f"输出目录: {result['output_dir']}")
                return True
            else:
                logger.error("❌ 网页生成失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 网页生成测试异常: {e}")
            return False 