#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
更新内容脚本
更新9月17日内容并生成9月18日新内容
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime, date

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.config import get_config
from src.scheduler.task_scheduler import TaskScheduler
from src.generators.web_generator import WebGenerator

async def update_content():
    """更新内容"""
    try:
        print("🚀 开始更新内容...")
        print("=" * 60)
        
        # 创建任务调度器
        scheduler = TaskScheduler()
        
        # 执行每日摘要任务（这会生成今天的内容）
        print("📅 生成今日内容...")
        await scheduler.daily_digest_task()
        
        print("\n🎉 内容更新完成！")
        print("📄 生成的文件:")
        print("   • output/index.html - 主页面")
        print("   • output/daily-*.html - 每日简报")
        print("   • output/archive.html - 归档页面")
        print("   • data/digest-*.json - 数据文件")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 更新失败: {e}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(update_content())
    sys.exit(0 if success else 1)
