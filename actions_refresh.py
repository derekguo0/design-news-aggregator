#!/usr/bin/env python3
"""
GitHub Actions 专用刷新脚本
针对云环境优化，确保在有限时间内完成资讯抓取和生成
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def main():
    """主函数：执行完整的资讯抓取和网站生成流程"""
    try:
        logger.info("🚀 GitHub Actions 自动刷新开始")
        start_time = datetime.now()
        
        # 检查环境
        logger.info(f"🌍 运行环境: GitHub Actions")
        logger.info(f"📁 工作目录: {os.getcwd()}")
        logger.info(f"🐍 Python 版本: {sys.version}")
        
        # 导入必要模块
        logger.info("📦 导入模块...")
        from src.scheduler.task_scheduler import TaskScheduler
        from src.config import get_config
        
        # 加载配置
        logger.info("⚙️ 加载配置...")
        config = get_config()
        
        # 创建任务调度器
        logger.info("🔄 创建任务调度器...")
        scheduler = TaskScheduler(config)
        
        # 执行每日摘要任务（包含爬取、处理、生成）
        logger.info("📰 开始执行每日摘要任务...")
        result = scheduler.daily_digest_task()
        
        if result:
            elapsed = datetime.now() - start_time
            logger.info(f"✅ 刷新任务完成! 耗时: {elapsed.total_seconds():.1f}秒")
            
            # 显示生成的文件
            output_dir = Path("output")
            if output_dir.exists():
                files = list(output_dir.glob("*.html"))
                logger.info(f"📄 生成了 {len(files)} 个HTML文件")
                
            data_dir = Path("data")
            if data_dir.exists():
                json_files = list(data_dir.glob("digest-*.json"))
                logger.info(f"💾 数据文件: {len(json_files)} 个")
                
            return True
        else:
            logger.error("❌ 刷新任务失败")
            return False
            
    except ImportError as e:
        logger.error(f"❌ 模块导入失败: {e}")
        logger.info("💡 尝试安装依赖: pip install -r requirements.txt")
        return False
    except Exception as e:
        logger.error(f"💥 刷新过程中发生错误: {str(e)}")
        import traceback
        logger.error(f"📋 错误详情:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    
    print("\n🎉 GitHub Actions 自动刷新完成!")
    print("📊 生成的内容将自动提交并触发 Vercel 重新部署")
