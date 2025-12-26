"""
网页生成器
将设计资讯转换为静态HTML页面
"""
import os
import json
import shutil
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger

from ..models import DailyDigest, NewsItem, CategorySummary
from ..config import get_config

class WebGenerator:
    """静态网页生成器"""
    
    def __init__(self, template_dir: str = "templates", output_dir: str = "output"):
        self.config = get_config()
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.data_dir = Path("data")
        
        # 确保目录存在
        self.template_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        
        # 初始化Jinja2环境
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        # 添加自定义过滤器
        self.jinja_env.filters['datetimeformat'] = self._datetime_format
        self.jinja_env.filters['dateformat'] = self._date_format
    
    def _datetime_format(self, value: datetime, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """日期时间格式化过滤器"""
        if value is None:
            return ""
        return value.strftime(format)
    
    def _date_format(self, value: date, format: str = '%Y年%m月%d日') -> str:
        """日期格式化过滤器"""
        if value is None:
            return ""
        return value.strftime(format)
    
    def save_daily_digest(self, digest: DailyDigest) -> str:
        """保存每日摘要到JSON文件"""
        try:
            filename = f"digest-{digest.date.strftime('%Y-%m-%d')}.json"
            file_path = self.data_dir / filename
            
            # 转换为JSON可序列化的格式
            digest_data = {
                'date': digest.date.isoformat(),
                'total_items': digest.total_items,
                'sources': digest.sources,
                'generated_at': digest.generated_at.isoformat(),
                'categories': []
            }
            
            for category in digest.categories:
                category_data = {
                    'category': category.category,
                    'count': category.count,
                    'items': []
                }
                
                for item in category.items:
                    item_data = {
                        'title': item.title,
                        'url': str(item.url),
                        'author': item.author,
                        'category': item.category,
                        'source': item.source,
                        'summary': item.summary,
                        'published_at': item.published_at.isoformat() if item.published_at else None
                    }
                    category_data['items'].append(item_data)
                
                digest_data['categories'].append(category_data)
            
            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(digest_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"每日摘要数据已保存: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"保存每日摘要数据失败: {e}")
            raise
    
    def load_daily_digest(self, date_str: str) -> Optional[DailyDigest]:
        """从JSON文件加载每日摘要"""
        try:
            filename = f"digest-{date_str}.json"
            file_path = self.data_dir / filename
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                digest_data = json.load(f)
            
            # 重建对象
            categories = []
            for cat_data in digest_data['categories']:
                items = []
                for item_data in cat_data['items']:
                    item = NewsItem(
                        title=item_data['title'],
                        url=item_data['url'],
                        author=item_data['author'],
                        category=item_data['category'],
                        source=item_data['source'],
                        summary=item_data['summary'],
                        published_at=datetime.fromisoformat(item_data['published_at']) if item_data['published_at'] else None
                    )
                    items.append(item)
                
                category = CategorySummary(
                    category=cat_data['category'],
                    items=items,
                    count=cat_data['count']
                )
                categories.append(category)
            
            digest = DailyDigest(
                date=datetime.fromisoformat(digest_data['date']),
                total_items=digest_data['total_items'],
                categories=categories,
                sources=digest_data['sources'],
                generated_at=datetime.fromisoformat(digest_data['generated_at'])
            )
            
            return digest
            
        except Exception as e:
            logger.error(f"加载每日摘要数据失败 {date_str}: {e}")
            return None
    
    def load_all_digests(self) -> List[DailyDigest]:
        """加载所有历史摘要数据"""
        try:
            digests = []
            
            # 扫描data目录中的所有digest-*.json文件
            for file_path in self.data_dir.glob("digest-*.json"):
                try:
                    # 从文件名提取日期
                    date_str = file_path.stem.replace('digest-', '')
                    digest = self.load_daily_digest(date_str)
                    if digest:
                        digests.append(digest)
                except Exception as e:
                    logger.warning(f"加载文件失败 {file_path}: {e}")
                    continue
            
            # 按日期排序（最新的在前）
            digests.sort(key=lambda x: x.date, reverse=True)
            
            logger.info(f"成功加载 {len(digests)} 个历史摘要")
            return digests
            
        except Exception as e:
            logger.error(f"加载历史摘要失败: {e}")
            return []

    def generate_daily_page(self, digest: DailyDigest, template_name: str = "daily.html") -> str:
        """生成每日资讯页面"""
        try:
            template = self.jinja_env.get_template(template_name)
            
            # 计算统计信息
            total_articles = sum(len(cat.items) for cat in digest.categories)
            
            # 计算来源统计
            sources = set()
            for category in digest.categories:
                for item in category.items:
                    sources.add(item.source)
            
            template_data = {
                'digest': digest,
                'date': digest.date,  # 添加date变量
                'date_str': digest.date.strftime('%Y年%m月%d日'),
                'categories': digest.categories,
                'total_items': total_articles,  # 修正变量名
                'categories_count': len(digest.categories),
                'sources_count': len(sources),
                'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', 'G-0CBGM51K1P')  # 使用环境变量或默认 ID
            }
            
            # 渲染HTML
            html_content = template.render(**template_data)
            
            # 保存文件
            filename = f"daily-{digest.date.strftime('%Y-%m-%d')}.html"
            output_path = self.output_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 保存摘要数据到JSON
            self.save_daily_digest(digest)
            
            logger.success(f"每日页面生成成功: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"生成每日页面失败: {e}")
            raise
    
    def generate_index_page(self, recent_digests: List[DailyDigest], template_name: str = "index.html") -> str:
        """生成首页"""
        try:
            template = self.jinja_env.get_template(template_name)
            
            # 统计信息
            total_items = sum(digest.total_items for digest in recent_digests)
            all_sources = set()
            for digest in recent_digests:
                all_sources.update(digest.sources)
            
            # 当日全部资讯（按发布时间排序）
            latest_items = []
            if recent_digests:
                latest_digest = recent_digests[0]
                # 收集当日所有资讯
                for category in latest_digest.categories:
                    latest_items.extend(category.items)
                
                # 按发布时间排序（最新的在前）
                latest_items = sorted(latest_items, 
                                    key=lambda x: x.published_at if x.published_at else datetime.min, 
                                    reverse=True)
            
            # 收集分类信息用于筛选器
            categories_summary = []
            if recent_digests:
                latest_digest = recent_digests[0]
                categories_summary = latest_digest.categories

            # 收集所有来源用于筛选器
            sources_list = sorted(list(all_sources))

            template_data = {
                'latest_items': latest_items,  # 当日全部资讯
                'categories_summary': categories_summary,  # 修改变量名
                'stats': {
                    'total_days': len(recent_digests),
                    'total_items': total_items,
                    'total_sources': len(all_sources),
                    'avg_items_per_day': round(total_items / len(recent_digests), 1) if recent_digests else 0
                },
                'generated_at': datetime.now(),
                'meta': {
                    'title': "Design Drip - 每日设计动态汇总",
                    'description': f"Design Drip汇聚全球设计资讯，每日更新。已收集{total_items}条来自{len(all_sources)}个优质设计网站的资讯",
                    'keywords': "设计资讯,设计师,创意,Dribbble,Behance,Design Milk,工业设计,建筑设计,Design Drip"
                },
                'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', 'G-0CBGM51K1P')  # 使用环境变量或默认 ID
            }
            
            html_content = template.render(**template_data)
            
            # 保存首页
            output_path = self.output_dir / "index.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.success(f"首页生成成功: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"生成首页失败: {e}")
            raise
    
    def generate_archive_page(self, all_digests: List[DailyDigest] = None, template_name: str = "archive.html") -> str:
        """生成归档页面"""
        try:
            template = self.jinja_env.get_template(template_name)
            
            # 如果没有提供历史数据，从文件加载
            if all_digests is None:
                all_digests = self.load_all_digests()
            
            # 按月份分组
            monthly_archives = {}
            for digest in all_digests:
                month_key = digest.date.strftime('%Y-%m')
                month_display = digest.date.strftime('%Y年%m月')
                
                if month_key not in monthly_archives:
                    monthly_archives[month_key] = {
                        'display': month_display,
                        'digests': [],
                        'total_items': 0
                    }
                
                monthly_archives[month_key]['digests'].append(digest)
                monthly_archives[month_key]['total_items'] += digest.total_items
            
            # 排序（最新的在前）
            sorted_archives = sorted(
                monthly_archives.items(), 
                key=lambda x: x[0], 
                reverse=True
            )
            
            template_data = {
                'digests': all_digests,  # 修改变量名为digests
                'monthly_archives': sorted_archives,
                'total_days': len(all_digests),
                'total_items': sum(digest.total_items for digest in all_digests),
                'generated_at': datetime.now(),
                'meta': {
                    'title': "资讯归档 - Design Drip",
                    'description': f"Design Drip设计资讯历史归档，共{len(all_digests)}天的资讯记录",
                    'keywords': "设计资讯归档,历史资讯,设计师,Design Drip"
                },
                'google_analytics_id': os.getenv('GOOGLE_ANALYTICS_ID', 'G-0CBGM51K1P')  # 使用环境变量或默认 ID
            }
            
            html_content = template.render(**template_data)
            
            output_path = self.output_dir / "archive.html"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.success(f"归档页面生成成功: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"生成归档页面失败: {e}")
            raise
    
    def copy_static_files(self, static_dir: str = "templates/static"):
        """复制静态文件（CSS、JS、图片等）"""
        static_path = Path(static_dir)
        if not static_path.exists():
            logger.warning(f"静态文件目录不存在: {static_path}")
            return
        
        output_static = self.output_dir / "static"
        
        try:
            if output_static.exists():
                shutil.rmtree(output_static)
            
            shutil.copytree(static_path, output_static)
            logger.info(f"静态文件复制成功: {output_static}")
            
        except Exception as e:
            logger.error(f"复制静态文件失败: {e}")
    
    def generate_sitemap(self, all_digests: List[DailyDigest], base_url: str = "https://your-domain.com") -> str:
        """生成网站地图"""
        try:
            sitemap_content = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            ]
            
            # 首页
            sitemap_content.append(f'''
    <url>
        <loc>{base_url}/</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>''')
            
            # 归档页
            sitemap_content.append(f'''
    <url>
        <loc>{base_url}/archive.html</loc>
        <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>''')
            
            # 每日页面
            for digest in all_digests:
                filename = f"daily-{digest.date.strftime('%Y-%m-%d')}.html"
                sitemap_content.append(f'''
    <url>
        <loc>{base_url}/{filename}</loc>
        <lastmod>{digest.date.strftime('%Y-%m-%d')}</lastmod>
        <changefreq>never</changefreq>
        <priority>0.6</priority>
    </url>''')
            
            sitemap_content.append('</urlset>')
            
            # 保存sitemap
            sitemap_path = self.output_dir / "sitemap.xml"
            with open(sitemap_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sitemap_content))
            
            logger.success(f"网站地图生成成功: {sitemap_path}")
            return str(sitemap_path)
            
        except Exception as e:
            logger.error(f"生成网站地图失败: {e}")
            raise
    
    def generate_rss_feed(self, recent_digests: List[DailyDigest], base_url: str = "https://your-domain.com") -> str:
        """生成RSS订阅源"""
        try:
            rss_content = [
                '<?xml version="1.0" encoding="UTF-8"?>',
                '<rss version="2.0">',
                '<channel>',
                '<title>Design Drip</title>',
                f'<link>{base_url}</link>',
                '<description>Design Drip每日设计资讯汇总，汇聚全球优质设计内容</description>',
                '<language>zh-cn</language>',
                f'<lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")}</lastBuildDate>'
            ]
            
            # 添加最近的资讯
            for digest in recent_digests[:10]:  # 最近10天
                link = f"{base_url}/daily-{digest.date.strftime('%Y-%m-%d')}.html"
                title = f"设计资讯日报 - {digest.date.strftime('%Y年%m月%d日')}"
                description = f"今日收集{digest.total_items}条设计资讯，来自{len(digest.sources)}个网站"
                
                rss_content.append(f'''
<item>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    <pubDate>{digest.date.strftime("%a, %d %b %Y 09:00:00 +0800")}</pubDate>
    <guid>{link}</guid>
</item>''')
            
            rss_content.extend(['</channel>', '</rss>'])
            
            # 保存RSS
            rss_path = self.output_dir / "rss.xml"
            with open(rss_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(rss_content))
            
            logger.success(f"RSS订阅源生成成功: {rss_path}")
            return str(rss_path)
            
        except Exception as e:
            logger.error(f"生成RSS订阅源失败: {e}")
            raise
    
    def generate_complete_site(self, digest: DailyDigest, recent_digests: List[DailyDigest] = None, base_url: str = "https://your-domain.com"):
        """生成完整网站"""
        logger.info("开始生成完整网站")
        
        try:
            # 加载所有历史数据用于归档
            all_digests = self.load_all_digests()
            
            # 确保当前digest包含在历史数据中
            digest_exists = any(d.date.date() == digest.date.date() for d in all_digests)
            if not digest_exists:
                all_digests.insert(0, digest)
                all_digests.sort(key=lambda x: x.date, reverse=True)
            
            # 如果没有提供recent_digests，使用最近7天的数据
            if recent_digests is None:
                recent_digests = all_digests[:7]  # 最近7天
            
            # 确保当前digest在recent_digests的首位（最新）
            if recent_digests and recent_digests[0].date.date() != digest.date.date():
                # 移除可能存在的重复项
                recent_digests = [d for d in recent_digests if d.date.date() != digest.date.date()]
                # 在开头插入当前digest
                recent_digests.insert(0, digest)
                # 保持最多7天
                recent_digests = recent_digests[:7]
            elif not recent_digests:
                recent_digests = [digest]
            
            # 复制静态文件
            self.copy_static_files()
            
            # 生成每日页面（这里会自动保存digest数据）
            daily_path = self.generate_daily_page(digest)
            
            # 生成首页
            index_path = self.generate_index_page(recent_digests)
            
            # 生成归档页（使用所有历史数据）
            archive_path = self.generate_archive_page(all_digests)
            
            # 生成sitemap
            sitemap_path = self.generate_sitemap(all_digests, base_url)
            
            # 生成RSS
            rss_path = self.generate_rss_feed(recent_digests, base_url)
            
            logger.success(f"完整网站生成成功，输出目录: {self.output_dir}")
            
            return {
                'output_dir': str(self.output_dir),
                'daily_page': daily_path,
                'index_page': index_path,
                'archive_page': archive_path,
                'sitemap': sitemap_path,
                'rss_feed': rss_path
            }
            
        except Exception as e:
            logger.error(f"生成完整网站失败: {e}")
            raise 