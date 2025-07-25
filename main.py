#!/usr/bin/env python3
"""
设计资讯聚合工具
主程序入口
"""
import asyncio
import argparse
import sys
from pathlib import Path
from loguru import logger

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import get_config, reload_config
from src.scheduler.task_scheduler import TaskScheduler

def setup_logging():
    """设置日志"""
    config = get_config()
    
    # 移除默认处理器
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sys.stdout,
        level=config.log.level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )
    
    # 添加文件输出
    logger.add(
        "logs/app.log",
        level=config.log.level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention=config.log.retention,
        compression="zip",
        encoding="utf-8"
    )

async def run_scheduler():
    """运行调度器"""
    scheduler = TaskScheduler()
    
    try:
        # 添加每日任务
        scheduler.add_daily_job()
        
        # 启动调度器
        scheduler.start()
        
        # 显示任务列表
        scheduler.list_jobs()
        
        logger.info("调度器正在运行，按 Ctrl+C 退出")
        
        # 保持运行
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("收到退出信号")
    except Exception as e:
        logger.error(f"调度器运行异常: {e}")
    finally:
        scheduler.stop()
        logger.info("程序已退出")

async def run_once():
    """立即执行一次任务"""
    scheduler = TaskScheduler()
    await scheduler.run_once()

async def test_sources():
    """测试所有资讯源"""
    scheduler = TaskScheduler()
    await scheduler.test_all_sources()

async def test_web_gen():
    """测试网页生成"""
    scheduler = TaskScheduler()
    await scheduler.test_web_generation()

async def test_all():
    """测试所有功能"""
    logger.info("开始完整功能测试")
    
    scheduler = TaskScheduler()
    
    # 测试网页生成
    web_gen_ok = await scheduler.test_web_generation()
    if not web_gen_ok:
        logger.error("网页生成测试失败，请检查配置")
        return False
    
    # 测试资讯源
    await scheduler.test_all_sources()
    
    # 执行一次完整流程
    logger.info("执行一次完整的爬取和生成流程")
    await scheduler.run_once()
    
    logger.success("完整功能测试完成")
    return True

def show_config():
    """显示当前配置"""
    config = get_config()
    
    logger.info("=== 当前配置 ===")
    logger.info(f"飞书App ID: {config.feishu.app_id[:8]}...")
    logger.info(f"文档标题前缀: {config.feishu.doc_title_prefix}")
    logger.info(f"调度时间: {config.scheduler.hour:02d}:{config.scheduler.minute:02d}")
    logger.info(f"时区: {config.scheduler.timezone}")
    logger.info(f"请求延迟: {config.crawler.request_delay}秒")
    logger.info(f"日志级别: {config.log.level}")
    
    logger.info(f"\n=== 资讯源配置 ({len(config.sources)}个) ===")
    for source in config.sources:
        status = "✅" if source.enabled else "❌"
        logger.info(f"{status} {source.name} ({source.type}) - {source.category} - 限制{source.limit}条")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="设计资讯聚合工具")
    parser.add_argument("command", nargs="?", choices=[
        "start", "run", "test-sources", "test-web", "test-all", "config", "once"
    ], help="执行的命令")
    
    parser.add_argument("--config-reload", action="store_true", help="重新加载配置")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 重新加载配置
    if args.config_reload:
        reload_config()
        logger.info("配置已重新加载")
    
    # 设置日志
    setup_logging()
    
    if args.verbose:
        logger.level = "DEBUG"
    
    logger.info("设计资讯聚合工具启动")
    
    # 检查配置
    try:
        config = get_config()
        logger.info("配置加载成功")
    except Exception as e:
        logger.error(f"配置加载失败: {e}")
        logger.error("请检查配置文件或环境变量设置")
        sys.exit(1)
    
    # 执行命令
    if args.command == "start" or args.command == "run":
        try:
            asyncio.run(run_scheduler())
        except KeyboardInterrupt:
            logger.info("程序被用户中断")
    
    elif args.command == "once":
        asyncio.run(run_once())
    
    elif args.command == "test-sources":
        asyncio.run(test_sources())
    
    elif args.command == "test-web":
        asyncio.run(test_web_gen())
    
    elif args.command == "test-all":
        asyncio.run(test_all())
    
    elif args.command == "config":
        show_config()
    
    else:
        # 显示帮助信息
        parser.print_help()
        print("\n使用示例:")
        print("  python main.py start           # 启动调度器")
        print("  python main.py once            # 立即执行一次")
        print("  python main.py test-all        # 测试所有功能")
        print("  python main.py test-sources    # 测试资讯源")
        print("  python main.py test-web       # 测试网页生成")
        print("  python main.py config          # 显示配置")
        print("\n首次使用请:")
        print("  1. 复制 config/.env.example 为 config/.env")
        print("  2. 填写飞书应用配置信息")
        print("  3. 运行 python main.py test-all 测试")

if __name__ == "__main__":
    main() 