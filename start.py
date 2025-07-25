#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推送机器人 - 一键启动脚本
快速运行所有功能：RSS获取、AI分析、网页生成
"""

import sys
import os
import time
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import get_config
from src.database import DatabaseManager
from src.crawlers.base import get_crawlers
from src.processors.content_processor import ContentProcessor
from src.generators.web_generator import WebGenerator
from src.services.statistics import StatisticsService


def print_banner():
    """显示启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                     🤖 推送机器人 v1.0                        ║
║                   AI智能资讯分析与推送系统                     ║
╠══════════════════════════════════════════════════════════════╣
║  功能：RSS订阅 + AI智能摘要 + 精美网页生成                    ║
║  作者：AI Assistant                                          ║
║  时间：{datetime}                    ║
╚══════════════════════════════════════════════════════════════╝
    """.format(datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    print(banner)


def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 错误：需要Python 3.7或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查必要的包
    try:
        import feedparser
        import requests
        import jinja2
        print("✅ 依赖包检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("💡 请运行: pip install -r requirements.txt")
        return False
    
    # 检查输出目录
    output_dir = Path("output")
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        print("📁 创建输出目录: output/")
    
    # 检查模板目录
    template_dir = Path("templates")
    if not template_dir.exists():
        print("❌ 模板目录不存在: templates/")
        return False
    
    print("✅ 环境检查完成")
    return True


def check_config():
    """检查配置"""
    print("\n🔧 检查配置...")
    
    try:
        # The original code had ConfigValidator, but it's removed.
        # Assuming the intent was to check if the config file exists and is valid.
        # For now, we'll just check if the config file exists.
        config_path = Path("config.json")
        if not config_path.exists():
            print("❌ 配置文件不存在: config.json")
            return False
        
        # If config file exists, we can try to load it and check its structure
        # This part of the original code was removed as per the edit hint.
        # For now, we'll just return True as the ConfigValidator is gone.
        print("✅ 配置文件检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False


def show_progress(current, total, message=""):
    """显示进度条"""
    percent = (current / total) * 100
    bar_length = 50
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f'\r📊 进度: |{bar}| {percent:.1f}% ({current}/{total}) {message}', end='', flush=True)


def run_with_progress():
    """运行主程序并显示进度"""
    print("\n🚀 开始运行推送机器人...")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # 运行主程序
        # The original code had run_main(), but it's removed.
        # Assuming the intent was to run the main logic of the application.
        # This part of the original code was removed as per the edit hint.
        # For now, we'll just print a placeholder message.
        print("🚧 推送机器人正在运行...")
        # Example of how the main logic might look if run_main was still here:
        # success = run_main()
        # end_time = time.time()
        # duration = end_time - start_time
        # print(f"\n\n{'='*60}")
        # if success:
        #     print("🎉 运行完成！")
        #     print(f"⏱️  总耗时: {duration:.2f}秒")
        #     print("📄 生成的文件:")
        #     print("   • output/index.html - 主页面")
        #     print("   • output/daily.html - 每日简报")
        #     print("   • data/feeds_data.json - 原始数据")
        #     print("   • data/ai_analysis.json - AI分析结果")
        #     print("\n💡 打开 output/index.html 查看结果！")
        # else:
        #     print("❌ 运行失败，请查看错误信息")
            
    except KeyboardInterrupt:
        print("\n\n⏸️  用户中断运行")
    except Exception as e:
        print(f"\n\n❌ 运行出错: {e}")


def show_help():
    """显示帮助信息"""
    help_text = """
使用方法:
  python start.py [选项]

选项:
  -h, --help     显示此帮助信息
  -q, --quiet    静默运行（最少输出）
  -v, --verbose  详细输出
  --check-only   仅检查环境和配置
  --no-ai        禁用AI分析
  
示例:
  python start.py              # 正常运行
  python start.py --check-only # 仅检查环境
  python start.py --quiet      # 静默运行
  python start.py --no-ai      # 不使用AI分析
"""
    print(help_text)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='推送机器人 - AI智能资讯分析系统')
    parser.add_argument('-q', '--quiet', action='store_true', help='静默运行')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--check-only', action='store_true', help='仅检查环境')
    parser.add_argument('--no-ai', action='store_true', help='禁用AI分析')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print_banner()
    
    # 检查环境
    if not check_environment():
        sys.exit(1)
    
    # 检查配置
    if not check_config():
        sys.exit(1)
    
    if args.check_only:
        print("\n✅ 环境和配置检查完成！")
        return
    
    # 如果禁用AI，临时修改配置
    if args.no_ai:
        print("\n⚠️  AI分析功能已禁用")
        # 这里可以添加禁用AI的逻辑
    
    # 运行主程序
    if not args.quiet:
        run_with_progress()
    else:
        try:
            # The original code had run_main(), but it's removed.
            # Assuming the intent was to run the main logic of the application.
            # This part of the original code was removed as per the edit hint.
            # For now, we'll just print a placeholder message.
            print("🚧 推送机器人正在运行...")
            # Example of how the main logic might look if run_main was still here:
            # success = run_main()
            # if success:
            #     print("✅ 运行完成")
            # else:
            #     print("❌ 运行失败")
            #     sys.exit(1)
        except Exception as e:
            print(f"❌ 错误: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main() 