#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
一键刷新启动脚本
启动刷新服务器并打开网页，实现完整的一键刷新体验
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

def print_banner():
    """显示启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  🔄 一键刷新资讯系统                          ║
║              点击网页中的"刷新资讯"按钮即可自动更新              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def start_refresh_server():
    """启动刷新服务器"""
    try:
        print("🚀 启动刷新服务器...")
        subprocess.run([sys.executable, 'refresh_server.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 刷新服务器启动失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  刷新服务器已停止")

def open_website():
    """打开网站"""
    time.sleep(2)  # 等待服务器启动
    output_dir = Path('output')
    index_file = output_dir / 'index.html'
    
    if index_file.exists():
        file_url = f"file://{index_file.absolute()}"
        print(f"🌐 打开网站: {file_url}")
        webbrowser.open(file_url)
    else:
        print("⚠️  网站文件不存在，正在生成...")
        # 先生成网站
        subprocess.run([sys.executable, 'simple_run.py'], check=True)
        if index_file.exists():
            file_url = f"file://{index_file.absolute()}"
            print(f"🌐 打开网站: {file_url}")
            webbrowser.open(file_url)

def main():
    """主函数"""
    print_banner()
    
    print("📝 使用说明:")
    print("1. 刷新服务器将在后台运行 (http://localhost:5001)")
    print("2. 网页将自动打开")
    print("3. 点击网页中的'🔄 刷新资讯'按钮即可自动更新")
    print("4. 按 Ctrl+C 停止服务")
    print("=" * 60)
    
    # 在后台线程中打开网站
    website_thread = threading.Thread(target=open_website)
    website_thread.daemon = True
    website_thread.start()
    
    # 启动刷新服务器（阻塞运行）
    start_refresh_server()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0) 