#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单运行脚本
用于一次性执行所有资讯爬取和处理任务
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.config import get_config
from src.scheduler.task_scheduler import TaskScheduler
from src.services.statistics import StatisticsService


async def run_once():
    """运行一次完整的任务流程"""
    try:
        # 创建任务调度器
        scheduler = TaskScheduler()
        
        print("🚀 开始执行资讯爬取和处理任务...")
        print("=" * 60)
        
        # 执行每日摘要任务
        await scheduler.daily_digest_task()
        
        print("\n🎉 任务执行完成！")
        print("📄 生成的文件:")
        print("   • output/index.html - 主页面")
        print("   • output/daily.html - 每日简报")
        print("   • output/archive.html - 归档页面")
        print("   • output/statistics.txt - 统计报告")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 任务执行失败: {e}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return False


def main():
    """主函数"""
    try:
        # 运行异步任务
        success = asyncio.run(run_once())
        return success
    except KeyboardInterrupt:
        print("\n⏸️  用户中断运行")
        return False
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 