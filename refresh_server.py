#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
刷新服务器
提供一键刷新资讯的Web API服务
"""

import os
import sys
import subprocess
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
from loguru import logger

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 全局状态
refresh_status = {
    'is_running': False,
    'last_refresh': None,
    'error': None
}

@app.route('/api/refresh', methods=['POST'])
def refresh_news():
    """刷新资讯API"""
    global refresh_status
    
    # 检查是否已经在运行
    if refresh_status['is_running']:
        return jsonify({
            'success': False,
            'message': '刷新正在进行中，请稍候...',
            'status': 'running'
        }), 409
    
    try:
        # 设置运行状态
        refresh_status['is_running'] = True
        refresh_status['error'] = None
        
        logger.info("开始执行资讯刷新...")
        
        # 在后台线程中执行刷新命令
        def run_refresh():
            try:
                # 执行刷新命令
                result = subprocess.run(
                    [sys.executable, 'simple_run.py'],
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5分钟超时
                )
                
                if result.returncode == 0:
                    refresh_status['last_refresh'] = datetime.now().isoformat()
                    refresh_status['error'] = None
                    logger.success("资讯刷新完成")
                else:
                    refresh_status['error'] = result.stderr or "执行失败"
                    logger.error(f"资讯刷新失败: {refresh_status['error']}")
                    
            except subprocess.TimeoutExpired:
                refresh_status['error'] = "执行超时（超过5分钟）"
                logger.error("资讯刷新超时")
            except Exception as e:
                refresh_status['error'] = str(e)
                logger.error(f"资讯刷新异常: {e}")
            finally:
                refresh_status['is_running'] = False
        
        # 启动后台线程
        thread = threading.Thread(target=run_refresh)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': '资讯刷新已开始，请稍候...',
            'status': 'started'
        })
        
    except Exception as e:
        refresh_status['is_running'] = False
        refresh_status['error'] = str(e)
        logger.error(f"启动刷新失败: {e}")
        
        return jsonify({
            'success': False,
            'message': f'启动失败: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取刷新状态"""
    return jsonify({
        'is_running': refresh_status['is_running'],
        'last_refresh': refresh_status['last_refresh'],
        'error': refresh_status['error']
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 启动刷新服务器...")
    print("📍 服务地址: http://localhost:5001")
    print("🔄 API接口: POST /api/refresh")
    print("📊 状态查询: GET /api/status")
    print("💡 在浏览器中打开 output/index.html 即可使用一键刷新功能")
    print("⏹️  按 Ctrl+C 停止服务")
    
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=False,
        threaded=True
    ) 