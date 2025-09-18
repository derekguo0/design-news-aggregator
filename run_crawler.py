#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
运行爬虫脚本
手动运行爬虫系统获取当天真实资讯
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.config import get_config
from src.scheduler.task_scheduler import TaskScheduler
from src.generators.web_generator import WebGenerator

async def run_crawler():
    """运行爬虫系统"""
    try:
        print("🚀 开始运行爬虫系统...")
        print("=" * 60)
        
        # 创建任务调度器
        scheduler = TaskScheduler()
        
        # 执行每日摘要任务（这会爬取真实资讯）
        print("📅 开始爬取今日资讯...")
        await scheduler.daily_digest_task()
        
        print("\n🎉 爬虫运行完成！")
        print("📄 生成的文件:")
        print("   • data/digest-*.json - 数据文件")
        print("   • output/daily-*.html - 每日页面")
        print("   • output/index.html - 首页")
        print("   • output/archive.html - 归档页面")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 爬虫运行失败: {e}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_crawler())
    sys.exit(0 if success else 1)
