#!/usr/bin/env python3
"""
GitHub Actions专用的内容刷新脚本
简化版本，专门为CI/CD环境优化
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.scheduler.task_scheduler import TaskScheduler

async def actions_refresh():
    """GitHub Actions环境专用的刷新功能"""
    try:
        print("🚀 GitHub Actions 开始生成最新内容...")
        print("=" * 60)
        
        # 初始化调度器
        scheduler = TaskScheduler()
        
        # 生成最新内容
        print(f"\n📅 开始生成 {datetime.now().strftime('%Y-%m-%d')} 的资讯内容")
        print("-" * 40)
        
        result = await scheduler.run_daily_task()
        
        if result['success']:
            print(f"✅ 内容生成成功!")
            print(f"📊 生成统计:")
            print(f"   • 总资讯数: {result.get('total_articles', 0)}")
            print(f"   • 资讯源数: {result.get('source_count', 0)}")
            print(f"   • 生成文件: {result.get('files_generated', [])}")
            print(f"   • 生成时间: {result.get('generation_time', 'N/A')}")
            
            return True
        else:
            print(f"❌ 内容生成失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"💥 执行过程出现异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🤖 GitHub Actions 内容生成器")
    print(f"🕒 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # 运行异步任务
    try:
        success = asyncio.run(actions_refresh())
        
        if success:
            print("\n🎉 GitHub Actions 内容生成完成!")
            print("📦 文件已生成到 output/ 和 data/ 目录")
            sys.exit(0)
        else:
            print("\n💥 GitHub Actions 内容生成失败!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 程序执行失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()