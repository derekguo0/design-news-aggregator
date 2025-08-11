import os
import json
import requests
from datetime import datetime
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """处理刷新请求 - 修复版本，兼容前端错误代码"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.end_headers()

        try:
            # 检查环境和Token
            is_vercel = bool(os.environ.get('VERCEL')) or bool(os.environ.get('VERCEL_ENV'))
            github_token = os.environ.get('GITHUB_TOKEN')
            
            print(f"🔍 环境检测: is_vercel={is_vercel}")
            print(f"🔑 GitHub Token: {'已配置' if github_token else '未配置'}")
            
            if is_vercel and github_token:
                # 触发GitHub Actions
                trigger_result = self._trigger_github_actions(github_token)
                
                if trigger_result['success']:
                    # 返回成功响应，包含ok字段兼容前端错误代码
                    response = {
                        'success': True,
                        'ok': True,  # 兼容前端错误代码中的response.ok检查
                        'message': '✅ GitHub Actions已成功触发！正在生成最新内容，请稍候2-3分钟后刷新页面查看新内容...',
                        'status': 'github_actions_triggered',
                        'timestamp': datetime.now().isoformat(),
                        'deployment_type': 'serverless',
                        'update_method': 'github_actions',
                        'estimated_completion': '2-3分钟',
                        'trigger_status': 'GitHub Actions workflow 已成功触发',
                        'cooldown_seconds': 180,
                        'frontend_fix': '已添加ok字段兼容前端错误代码'
                    }
                else:
                    response = {
                        'success': False,
                        'ok': False,
                        'message': f'⚠️ GitHub Actions触发失败: {trigger_result["message"]}',
                        'status': 'trigger_failed',
                        'timestamp': datetime.now().isoformat(),
                        'deployment_type': 'serverless',
                        'error_details': trigger_result['message']
                    }
            else:
                # 环境变量未配置
                response = {
                    'success': False,
                    'ok': False,
                    'message': '⚠️ 环境配置不完整，请检查GITHUB_TOKEN设置',
                    'status': 'configuration_error',
                    'timestamp': datetime.now().isoformat(),
                    'deployment_type': 'serverless',
                    'debug_info': {
                        'is_vercel': is_vercel,
                        'has_github_token': bool(github_token)
                    }
                }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'success': False,
                'ok': False,
                'message': f'服务器内部错误: {str(e)}',
                'status': 'server_error',
                'timestamp': datetime.now().isoformat()
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

    def _trigger_github_actions(self, github_token):
        """触发GitHub Actions工作流"""
        try:
            repo_name = os.environ.get('GITHUB_REPOSITORY', 'derekguo0/design-news-aggregator')
            workflow_dispatch_url = f"https://api.github.com/repos/{repo_name}/actions/workflows/deploy.yml/dispatches"
            
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'X-GitHub-Api-Version': '2022-11-28'
            }
            
            data = {
                'ref': 'main'
            }
            
            response = requests.post(workflow_dispatch_url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 204:
                return {
                    'success': True,
                    'message': 'GitHub Actions workflow successfully triggered'
                }
            else:
                return {
                    'success': False,
                    'message': f'GitHub API error: {response.status_code} - {response.text}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': 'GitHub API request timeout'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'message': 'Cannot connect to GitHub API'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}'
            }

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
