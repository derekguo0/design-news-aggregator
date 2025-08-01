from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import os
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # 检查是否在Vercel环境
            is_vercel = os.environ.get('VERCEL', False)
            
            if is_vercel:
                # 在Vercel环境中，触发GitHub Actions自动更新
                response = {
                    'success': True,
                    'message': '正在触发自动更新，请稍候2-3分钟后刷新页面查看新内容...',
                    'status': 'github_actions_triggered',
                    'timestamp': datetime.now().isoformat(),
                    'deployment_type': 'serverless',
                    'update_method': 'github_actions',
                    'estimated_completion': '2-3分钟'
                }
                
                # 尝试触发GitHub Actions（如果配置了webhook）
                try:
                    self._trigger_github_actions()
                except Exception as e:
                    print(f"触发GitHub Actions失败: {e}")
                    # 即使失败也继续，用户可以手动触发
                    
            else:
                # 本地环境，返回提示用户使用本地刷新服务器
                response = {
                    'success': False,
                    'message': '线上版本需要使用GitHub Actions更新。请在本地使用刷新服务器，或等待自动定时更新。',
                    'status': 'local_refresh_required',
                    'timestamp': datetime.now().isoformat(),
                    'deployment_type': 'static',
                    'instructions': {
                        'local_refresh': '本地运行: python3 start_with_refresh.py',
                        'manual_trigger': '在GitHub仓库中手动触发Actions',
                        'automatic_update': '每天00:00和12:00(UTC)自动更新'
                    }
                }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                'success': False,
                'message': f'刷新请求失败: {str(e)}',
                'status': 'error',
                'deployment_type': 'unknown'
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def _trigger_github_actions(self):
        """尝试触发GitHub Actions（需要配置webhook或使用GitHub API）"""
        # 这里可以添加GitHub API调用来触发workflow
        # 需要GITHUB_TOKEN环境变量
        github_token = os.environ.get('GITHUB_TOKEN')
        repo_name = os.environ.get('GITHUB_REPOSITORY', 'derekguo0/design-news-aggregator')
        
        if github_token:
            # 触发workflow dispatch
            url = f"https://api.github.com/repos/{repo_name}/actions/workflows/deploy.yml/dispatches"
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            data = {'ref': 'main'}
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 204:
                print("✅ GitHub Actions已成功触发")
            else:
                print(f"❌ 触发GitHub Actions失败: {response.status_code}")
        else:
            print("⚠️  未配置GITHUB_TOKEN，无法自动触发更新")
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 