#!/usr/bin/env python3
"""
带历史补全功能的刷新脚本
在生成最新内容之前自动检查并补全缺失的历史日期
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.scheduler.task_scheduler import TaskScheduler
from src.services.backfill_service import BackfillService
from loguru import logger


async def refresh_with_auto_backfill():
    """执行带自动补全功能的刷新"""
    try:
        print("🚀 开始执行智能刷新（包含历史补全）...")
        print("=" * 60)
        
        # 初始化服务
        backfill_service = BackfillService()
        scheduler = TaskScheduler()
        
        # 步骤1: 历史内容补全
        print("\n📋 步骤1: 检查历史内容完整性")
        print("-" * 40)
        
        backfill_result = backfill_service.auto_backfill(max_days_back=30)
        
        if backfill_result['success']:
            if backfill_result['action'] == 'backfilled':
                print(f"✅ {backfill_result['message']}")
                print(f"📊 补全详情:")
                print(f"   • 检查范围: {backfill_result['date_range']}")
                print(f"   • 缺失日期: {backfill_result['missing_count']} 个")
                print(f"   • 创建文件: {backfill_result['created_files']} 个")
                print(f"   • 缺失日期列表: {', '.join(backfill_result['missing_dates'])}")
                
                # 如果有补全内容，稍等一下让用户看到结果
                print("\\n⏳ 历史补全完成，继续生成最新内容...")
                await asyncio.sleep(2)
            else:
                print(f"ℹ️  {backfill_result['message']}")
        else:
            print(f"⚠️  {backfill_result['message']}")
            print("继续执行正常刷新流程...")
        
        # 步骤2: 执行正常的每日摘要任务（包含最新内容生成）
        print("\\n🔄 步骤2: 生成最新资讯内容")
        print("-" * 40)
        
        await scheduler.daily_digest_task()
        
        print("\\n🎉 智能刷新完成！")
        print("=" * 60)
        print("📁 生成的文件:")
        print("   • output/index.html - 首页")
        print("   • output/daily-{today}.html - 今日页面".format(today=datetime.now().strftime('%Y-%m-%d')))
        print("   • output/archive.html - 归档页面（包含历史补全）")
        print("   • output/rss.xml - RSS订阅源")
        
        if backfill_result.get('created_files', 0) > 0:
            print("\\n💡 温馨提示:")
            print("   历史内容已自动补全，归档页面现在更加完整！")
            print("   补全的日期显示为占位页面，保持了时间线的连续性。")
        
    except Exception as e:
        logger.error(f"刷新执行失败: {e}")
        print(f"\\n❌ 刷新失败: {e}")
        return False
    
    return True


async def main():
    """主函数"""
    try:
        success = await refresh_with_auto_backfill()
        if success:
            print("\\n✨ 全部完成！您可以在浏览器中打开 output/index.html 查看最新内容。")
        else:
            print("\\n💥 执行过程中遇到问题，请检查日志。")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\\n⏹️  用户中断操作")
        sys.exit(0)
    except Exception as e:
        print(f"\\n💥 执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # 设置日志
    logger.add("logs/refresh_backfill.log", rotation="1 week", retention="1 month")
    
    # 运行主函数
    asyncio.run(main())