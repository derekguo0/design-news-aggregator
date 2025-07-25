"""
基础爬虫类
定义通用的爬虫接口和功能
"""
import time
import asyncio
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import feedparser
from loguru import logger

from ..models import NewsItem
from ..config import get_config, SourceConfig

class BaseCrawler(ABC):
    """基础爬虫抽象类"""
    
    def __init__(self, source_config: SourceConfig):
        self.config = source_config
        self.app_config = get_config()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """创建HTTP会话"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': self.app_config.crawler.user_agent
        })
        return session
    
    @abstractmethod
    def crawl(self) -> List[NewsItem]:
        """爬取资讯内容 - 子类必须实现"""
        pass
    
    def _delay(self):
        """请求间延迟"""
        time.sleep(self.app_config.crawler.request_delay)
    
    def _get_page_content(self, url: str) -> Optional[str]:
        """获取页面内容"""
        try:
            self._delay()
            response = self.session.get(
                url, 
                timeout=self.app_config.crawler.request_timeout
            )
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

class WebCrawler(BaseCrawler):
    """网页爬虫"""
    
    def crawl(self) -> List[NewsItem]:
        """爬取网页内容"""
        logger.info(f"开始爬取 {self.config.name} - {self.config.url}")
        
        content = self._get_page_content(self.config.url)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'html.parser')
        items = []
        
        try:
            # 根据配置的选择器提取内容
            item_elements = soup.select(self.config.selectors.item)[:self.config.limit]
            
            for element in item_elements:
                try:
                    item = self._extract_item(element, soup)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to extract item from {self.config.name}: {e}")
                    continue
            
            logger.success(f"成功爬取 {self.config.name}: {len(items)} 条资讯")
            
        except Exception as e:
            logger.error(f"Failed to parse content from {self.config.name}: {e}")
        
        return items
    
    def _extract_item(self, element, soup: BeautifulSoup) -> Optional[NewsItem]:
        """从元素中提取资讯条目"""
        try:
            # 提取标题
            title_elem = element.select_one(self.config.selectors.title)
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            
            # 提取链接
            link_elem = element.select_one(self.config.selectors.link)
            if not link_elem:
                return None
            url = link_elem.get('href', '')
            
            # 处理相对链接
            if url.startswith('/'):
                from urllib.parse import urljoin
                url = urljoin(self.config.url, url)
            
            # 提取作者
            author = None
            if self.config.selectors.author:
                author_elem = element.select_one(self.config.selectors.author)
                if author_elem:
                    author = author_elem.get_text(strip=True)
            
            # 提取图片
            image_url = None
            if self.config.selectors.image:
                img_elem = element.select_one(self.config.selectors.image)
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src')
                    if image_url and image_url.startswith('/'):
                        from urllib.parse import urljoin
                        image_url = urljoin(self.config.url, image_url)
            
            # 提取统计数据
            stats = {}
            if self.config.selectors.stats:
                stats_elem = element.select_one(self.config.selectors.stats)
                if stats_elem:
                    stats['stats'] = stats_elem.get_text(strip=True)
            
            if self.config.selectors.points:
                points_elem = element.select_one(self.config.selectors.points)
                if points_elem:
                    stats['points'] = points_elem.get_text(strip=True)
            
            return NewsItem(
                title=title,
                url=url,
                author=author,
                category=self.config.category,
                source=self.config.name,
                image_url=image_url,
                stats=stats if stats else None
            )
            
        except Exception as e:
            logger.warning(f"Error extracting item: {e}")
            return None

class RSSCrawler(BaseCrawler):
    """RSS爬虫"""
    
    def crawl(self) -> List[NewsItem]:
        """爬取RSS内容"""
        logger.info(f"开始爬取RSS {self.config.name} - {self.config.url}")
        
        try:
            self._delay()
            feed = feedparser.parse(self.config.url)
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning for {self.config.name}: {feed.bozo_exception}")
            
            items = []
            entries = feed.entries[:self.config.limit]
            
            for entry in entries:
                try:
                    item = self._extract_rss_item(entry)
                    if item:
                        items.append(item)
                except Exception as e:
                    logger.warning(f"Failed to extract RSS item from {self.config.name}: {e}")
                    continue
            
            logger.success(f"成功爬取RSS {self.config.name}: {len(items)} 条资讯")
            return items
            
        except Exception as e:
            logger.error(f"Failed to parse RSS from {self.config.name}: {e}")
            return []
    
    def _extract_rss_item(self, entry) -> Optional[NewsItem]:
        """从RSS条目中提取资讯"""
        try:
            title = entry.get('title', '').strip()
            url = entry.get('link', '').strip()
            
            if not title or not url:
                return None
            
            # 提取作者
            author = entry.get('author') or entry.get('dc_creator')
            
            # 提取摘要
            summary = entry.get('summary') or entry.get('description', '')
            if summary:
                # 清理HTML标签
                soup = BeautifulSoup(summary, 'html.parser')
                summary = soup.get_text(strip=True)
                # 限制摘要长度
                if len(summary) > 200:
                    summary = summary[:200] + "..."
            
            # 提取发布时间
            published_at = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                import calendar
                published_at = datetime.fromtimestamp(
                    calendar.timegm(entry.published_parsed)
                )
            
            # 提取标签
            tags = []
            if hasattr(entry, 'tags'):
                tags = [tag.term for tag in entry.tags if hasattr(tag, 'term')]
            
            return NewsItem(
                title=title,
                url=url,
                author=author,
                category=self.config.category,
                source=self.config.name,
                summary=summary,
                tags=tags,
                published_at=published_at
            )
            
        except Exception as e:
            logger.warning(f"Error extracting RSS item: {e}")
            return None

def create_crawler(source_config: SourceConfig) -> BaseCrawler:
    """工厂函数：根据配置创建对应的爬虫"""
    if source_config.type == 'web':
        return WebCrawler(source_config)
    elif source_config.type == 'rss':
        return RSSCrawler(source_config)
    else:
        raise ValueError(f"Unsupported crawler type: {source_config.type}") 