import os
import json
import subprocess
import tempfile
from datetime import datetime
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """处理手动刷新请求"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()

        github_token = os.environ.get('GITHUB_TOKEN')
        repo_name = os.environ.get('GITHUB_REPOSITORY', 'derekguo0/design-news-aggregator')
        
        if not github_token:
            response = {
                'success': False,
                'message': '未配置GITHUB_TOKEN环境变量',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return

        try:
            # 触发简化的刷新脚本
            result = self._trigger_simple_refresh(github_token, repo_name)
            
            response = {
                'success': True,
                'message': '内容刷新已完成',
                'details': result,
                'timestamp': datetime.now().isoformat(),
                'next_steps': '页面将在30秒后自动刷新以显示最新内容'
            }
            
        except Exception as e:
            response = {
                'success': False,
                'message': f'刷新失败: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

    def _trigger_simple_refresh(self, github_token, repo_name):
        """触发简化的内容刷新"""
        
        # 在Vercel serverless环境中，我们使用GitHub API触发一个简单的workflow
        import requests
        
        # 触发GitHub Actions工作流
        workflow_url = f"https://api.github.com/repos/{repo_name}/actions/workflows/deploy.yml/dispatches"
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        
        data = {
            'ref': 'main',
            'inputs': {
                'manual_trigger': 'true',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        response = requests.post(workflow_url, headers=headers, json=data, timeout=10)
        
        if response.status_code == 204:
            return {
                'github_actions': 'triggered',
                'message': 'GitHub Actions工作流已成功触发',
                'workflow_url': f'https://github.com/{repo_name}/actions'
            }
        else:
            raise Exception(f'GitHub API响应错误: {response.status_code} - {response.text}')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
