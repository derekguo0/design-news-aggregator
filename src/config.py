"""
配置管理模块
使用 Pydantic 进行配置验证和类型检查
"""
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SelectorConfig(BaseModel):
    """CSS选择器配置"""
    item: str
    title: str
    author: Optional[str] = None
    link: str
    image: Optional[str] = None
    stats: Optional[str] = None
    points: Optional[str] = None

class SourceConfig(BaseModel):
    """资讯源配置"""
    name: str
    url: str
    type: str = Field(..., pattern="^(web|rss)$")
    category: str
    selectors: Optional[SelectorConfig] = None
    enabled: bool = True
    limit: int = Field(default=10, ge=1, le=50)
    
    @validator('selectors')
    def validate_selectors(cls, v, values):
        if values.get('type') == 'web' and v is None:
            raise ValueError('Web sources must have selectors configured')
        return v

class FeishuConfig(BaseModel):
    """飞书配置"""
    app_id: str
    app_secret: str
    tenant_access_token: Optional[str] = None
    folder_token: Optional[str] = None
    doc_title_prefix: str = "设计资讯日报"
    
    class Config:
        env_prefix = "FEISHU_"

class CrawlerConfig(BaseModel):
    """爬虫配置"""
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    request_timeout: int = 30
    request_delay: float = 1.0

class SchedulerConfig(BaseModel):
    """调度器配置"""
    hour: int = 9
    minute: int = 0
    timezone: str = "Asia/Shanghai"

class LogConfig(BaseModel):
    """日志配置"""
    level: str = "INFO"
    retention: str = "30 days"

class AIConfig(BaseModel):
    """AI分析配置"""
    enabled: bool = True
    api_key: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 150
    temperature: float = 0.7
    
    class Config:
        env_prefix = "AI_"

class AppConfig(BaseModel):
    """应用总配置"""
    feishu: FeishuConfig
    crawler: CrawlerConfig
    scheduler: SchedulerConfig
    log: LogConfig
    ai: AIConfig
    sources: List[SourceConfig]
    
    @classmethod
    def load_from_files(cls) -> "AppConfig":
        """从配置文件加载配置"""
        # 获取项目根目录
        project_root = Path(__file__).parent.parent
        
        # 加载资讯源配置
        sources_file = project_root / "config" / "sources.json"
        if not sources_file.exists():
            raise FileNotFoundError(f"Sources config file not found: {sources_file}")
            
        with open(sources_file, 'r', encoding='utf-8') as f:
            sources_data = json.load(f)
        
        # 从环境变量创建配置实例
        config_data = {
            "feishu": FeishuConfig(
                app_id=os.getenv("FEISHU_APP_ID", ""),
                app_secret=os.getenv("FEISHU_APP_SECRET", ""),
                tenant_access_token=os.getenv("FEISHU_TENANT_ACCESS_TOKEN"),
                folder_token=os.getenv("FEISHU_FOLDER_TOKEN"),
                doc_title_prefix=os.getenv("FEISHU_DOC_TITLE_PREFIX", "设计资讯日报")
            ),
            "crawler": CrawlerConfig(
                user_agent=os.getenv("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"),
                request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
                request_delay=float(os.getenv("REQUEST_DELAY", "1.0"))
            ),
            "scheduler": SchedulerConfig(
                hour=int(os.getenv("SCHEDULE_HOUR", "9")),
                minute=int(os.getenv("SCHEDULE_MINUTE", "0")),
                timezone=os.getenv("TIMEZONE", "Asia/Shanghai")
            ),
            "log": LogConfig(
                level=os.getenv("LOG_LEVEL", "INFO"),
                retention=os.getenv("LOG_RETENTION", "30 days")
            ),
            "ai": AIConfig(
                enabled=os.getenv("AI_ENABLED", "true").lower() == "true",
                api_key=os.getenv("OPENAI_API_KEY") or os.getenv("AI_API_KEY"),
                model=os.getenv("AI_MODEL", "gpt-3.5-turbo"),
                max_tokens=int(os.getenv("AI_MAX_TOKENS", "150")),
                temperature=float(os.getenv("AI_TEMPERATURE", "0.7"))
            ),
            "sources": [SourceConfig(**source) for source in sources_data["sources"]]
        }
        
        return cls(**config_data)

# 全局配置实例
config: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """获取全局配置实例"""
    global config
    if config is None:
        config = AppConfig.load_from_files()
    return config

def reload_config() -> AppConfig:
    """重新加载配置"""
    global config
    config = AppConfig.load_from_files()
    return config 