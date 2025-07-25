"""
内容处理模块
负责对爬取的内容进行清洗、去重和聚合
"""
from typing import List, Dict, Set
from datetime import datetime, date
from collections import defaultdict
from loguru import logger

from ..models import NewsItem, CategorySummary, DailyDigest

class ContentProcessor:
    """内容处理器"""
    
    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.seen_titles: Set[str] = set()
    
    def process_items(self, items: List[NewsItem]) -> List[NewsItem]:
        """处理和清洗资讯条目"""
        logger.info(f"开始处理 {len(items)} 条资讯")
        
        # 去重
        unique_items = self._deduplicate(items)
        logger.info(f"去重后剩余 {len(unique_items)} 条资讯")
        
        # 内容清洗
        cleaned_items = self._clean_items(unique_items)
        logger.info(f"清洗后剩余 {len(cleaned_items)} 条资讯")
        
        return cleaned_items
    
    def _deduplicate(self, items: List[NewsItem]) -> List[NewsItem]:
        """去重处理"""
        unique_items = []
        
        for item in items:
            # URL去重
            url_key = str(item.url).lower().strip()
            if url_key in self.seen_urls:
                continue
            
            # 标题去重 (简单的相似度检查)
            title_key = self._normalize_title(item.title)
            if title_key in self.seen_titles:
                continue
            
            self.seen_urls.add(url_key)
            self.seen_titles.add(title_key)
            unique_items.append(item)
        
        return unique_items
    
    def _normalize_title(self, title: str) -> str:
        """标题标准化，用于去重"""
        # 转换为小写，移除标点符号和空格
        import re
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def _clean_items(self, items: List[NewsItem]) -> List[NewsItem]:
        """内容清洗"""
        cleaned_items = []
        
        for item in items:
            # 清理标题
            if not item.title or len(item.title.strip()) < 5:
                continue
            
            item.title = self._clean_text(item.title)
            
            # 清理摘要
            if item.summary:
                item.summary = self._clean_text(item.summary)
                if len(item.summary) < 10:
                    item.summary = None
            
            # 清理作者名
            if item.author:
                item.author = self._clean_text(item.author)
                if len(item.author) > 50:  # 防止异常长的作者名
                    item.author = item.author[:50] + "..."
            
            cleaned_items.append(item)
        
        return cleaned_items
    
    def _clean_text(self, text: str) -> str:
        """文本清理"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        import re
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 移除特殊字符
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        return text
    
    def aggregate_by_category(self, items: List[NewsItem]) -> List[CategorySummary]:
        """按分类聚合资讯"""
        category_dict = defaultdict(list)
        
        for item in items:
            category_dict[item.category].append(item)
        
        # 定义分类显示顺序，"行业资讯"放在最后
        category_order = [
            "用户体验设计",
            "用户体验研究",
            "产品设计",
            "网页设计",
            "产品发现",  # 移动到网页设计后面
            "设计教程",
            "设计资讯",
            "设计资源",
            "前端设计",
            "原型设计",
            "游戏设计",
            "行业资讯"  # 放在最后
        ]
        
        # 按定义的顺序排列分类，未定义的分类按条目数排序后插入
        ordered_categories = []
        remaining_categories = dict(category_dict)
        
        # 按预定义顺序添加分类
        for category_name in category_order:
            if category_name in remaining_categories:
                ordered_categories.append((category_name, remaining_categories[category_name]))
                del remaining_categories[category_name]
        
        # 添加剩余的未定义分类（按条目数排序）
        remaining_sorted = sorted(
            remaining_categories.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        ordered_categories.extend(remaining_sorted)
        
        return [
            CategorySummary(category=category, items=items)
            for category, items in ordered_categories
        ]
    
    def create_daily_digest(self, items: List[NewsItem], target_date: date = None) -> DailyDigest:
        """创建每日摘要"""
        if target_date is None:
            target_date = date.today()
        
        # 包含最近几天的资讯，不要过于严格的日期过滤
        from datetime import timedelta
        
        today_items = []
        cutoff_date = target_date - timedelta(days=3)  # 包含最近3天的资讯
        
        for item in items:
            if item.published_at:
                # 包含最近3天的资讯
                if item.published_at.date() >= cutoff_date:
                    today_items.append(item)
            else:
                # 没有发布时间的默认包含（如Product Hunt等）
                today_items.append(item)
        
        # 如果仍然没有内容，使用全部资讯
        if not today_items:
            today_items = items
        
        # 按分类聚合
        categories = self.aggregate_by_category(today_items)
        
        return DailyDigest(
            date=datetime.combine(target_date, datetime.min.time()),
            categories=categories
        )
    
    def generate_summary_stats(self, digest: DailyDigest) -> Dict[str, any]:
        """生成摘要统计信息"""
        stats = {
            "total_items": digest.total_items,
            "categories_count": len(digest.categories),
            "sources_count": len(digest.sources),
            "categories": [],
            "sources": digest.sources
        }
        
        for category in digest.categories:
            category_stats = {
                "name": category.category,
                "count": category.count,
                "top_sources": self._get_top_sources_for_category(category)
            }
            stats["categories"].append(category_stats)
        
        return stats
    
    def _get_top_sources_for_category(self, category: CategorySummary) -> List[Dict[str, any]]:
        """获取分类下的热门来源"""
        source_count = defaultdict(int)
        for item in category.items:
            source_count[item.source] += 1
        
        return [
            {"source": source, "count": count}
            for source, count in sorted(source_count.items(), key=lambda x: x[1], reverse=True)
        ] 