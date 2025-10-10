#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions专用的内容刷新脚本
简化版本，避免复杂的依赖问题
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.scheduler.task_scheduler import TaskScheduler
import asyncio

async def run_full_generation():
    scheduler = TaskScheduler()
    await scheduler.run_once()

def create_simple_content():
    """执行完整的内容生成流程"""
    try:
        print("🚀 开始完整的内容生成流程...")
        
        # 获取今天的日期
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"📅 生成日期: {today}")
        
        # 确保目录存在
        output_dir = Path("output")
        data_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        data_dir.mkdir(exist_ok=True)
        
        # 直接使用系统完整生成流程（不创建测试数据）
        print("🚀 调用TaskScheduler完整爬取和生成...")
        asyncio.run(run_full_generation())
        
        print(f"\n🎉 内容生成完成！")
        print(f"📊 系统已自动:")
        print(f"   • 爬取所有启用的资讯源")
        print(f"   • 处理并去重内容")
        print(f"   • 生成每日摘要")
        print(f"   • 生成所有HTML页面")
        print(f"   • 更新RSS和Sitemap")
        
        return True
        
    except Exception as e:
        print(f"❌ 内容生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🤖 GitHub Actions 内容刷新脚本")
    print(f"🕒 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    success = create_simple_content()
    
    if success:
        print("\n✅ 脚本执行成功！")
        sys.exit(0)
    else:
        print("\n❌ 脚本执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()