"""
数据模型定义
定义设计资讯条目和聚合结果的数据结构
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

class NewsItem(BaseModel):
    """新闻条目模型"""
    title: str = Field(..., description="标题")
    url: HttpUrl = Field(..., description="链接")
    source: str = Field(..., description="来源")
    category: str = Field("其他", description="分类")
    author: Optional[str] = Field(None, description="作者")
    summary: Optional[str] = Field(None, description="摘要")
    published_at: Optional[datetime] = Field(None, description="发布时间")
    
    class Config:
        arbitrary_types_allowed = True

class CategorySummary(BaseModel):
    """分类汇总"""
    category: str = Field(..., description="分类名称")
    items: List[NewsItem] = Field(..., description="该分类下的资讯条目")
    count: int = Field(0, description="条目数量")
    
    def __init__(self, **data):
        if 'count' not in data:
            data['count'] = len(data.get('items', []))
        super().__init__(**data)

class DailyDigest(BaseModel):
    """每日资讯摘要"""
    date: datetime = Field(..., description="日期")
    total_items: int = Field(0, description="总条目数")
    categories: List[CategorySummary] = Field(..., description="分类汇总")
    sources: List[str] = Field(default_factory=list, description="资讯源列表")
    generated_at: datetime = Field(default_factory=datetime.now, description="生成时间")
    
    def __init__(self, **data):
        if 'total_items' not in data:
            data['total_items'] = sum(cat.count for cat in data.get('categories', []))
        if 'sources' not in data:
            sources = set()
            for cat in data.get('categories', []):
                for item in cat.items:
                    sources.add(item.source)
            data['sources'] = list(sources)
        super().__init__(**data)
    
    def to_feishu_blocks(self) -> List[Dict[str, Any]]:
        """转换为飞书文档块格式"""
        blocks = []
        
        # 标题
        title = f"设计资讯日报 - {self.date.strftime('%Y年%m月%d日')}"
        blocks.append({
            "block_type": "heading1",
            "heading1": {
                "elements": [{"text_run": {"content": title}}]
            }
        })
        
        # 概览信息
        overview = f"📊 今日共收集 {self.total_items} 条设计资讯，来源于 {len(self.sources)} 个网站"
        blocks.append({
            "block_type": "text",
            "text": {
                "elements": [{"text_run": {"content": overview}}],
                "style": {"text_color": "blue"}
            }
        })
        
        # 分类内容
        for category in self.categories:
            if category.count == 0:
                continue
                
            # 分类标题
            category_title = f"🎨 {category.category} ({category.count}条)"
            blocks.append({
                "block_type": "heading2", 
                "heading2": {
                    "elements": [{"text_run": {"content": category_title}}]
                }
            })
            
            # 分类内容项
            for i, item in enumerate(category.items, 1):
                # 构建条目内容
                content_parts = [f"{i}. **{item.title}**"]
                
                if item.author:
                    content_parts.append(f"   👤 作者: {item.author}")
                
                if item.summary:
                    content_parts.append(f"   📝 {item.summary}")
                
                content_parts.append(f"   🔗 [查看详情]({item.url})")
                content_parts.append(f"   📍 来源: {item.source}")
                
                content = "\n".join(content_parts)
                
                blocks.append({
                    "block_type": "text",
                    "text": {
                        "elements": [{"text_run": {"content": content}}]
                    }
                })
                
                # 添加间隔
                if i < len(category.items):
                    blocks.append({
                        "block_type": "text",
                        "text": {
                            "elements": [{"text_run": {"content": ""}}]
                        }
                    })
        
        # 页脚信息
        footer = f"⏰ 生成时间: {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}"
        blocks.append({
            "block_type": "text",
            "text": {
                "elements": [{"text_run": {"content": footer}}],
                "style": {"text_color": "grey"}
            }
        })
        
        return blocks 