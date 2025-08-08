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
            
            # 检查是否在Vercel环境 - 更准确的检测
            is_vercel = bool(os.environ.get('VERCEL')) or bool(os.environ.get('VERCEL_ENV'))
            github_token = os.environ.get('GITHUB_TOKEN')
            
            print(f"🔍 环境检测: VERCEL={os.environ.get('VERCEL')}, VERCEL_ENV={os.environ.get('VERCEL_ENV')}, is_vercel={is_vercel}")
            print(f"🔑 GitHub Token: {'已配置' if github_token else '未配置'}")
            
            if is_vercel:
                # 尝试触发GitHub Actions
                trigger_result = self._trigger_github_actions()
                
                if trigger_result['success']:
                    response = {
                        'success': True,
                        'message': '✅ GitHub Actions已成功触发！正在生成最新内容，请稍候2-3分钟后刷新页面查看新内容...',
                        'status': 'github_actions_triggered',
                        'timestamp': datetime.now().isoformat(),
                        'deployment_type': 'serverless',
                        'update_method': 'github_actions',
                        'estimated_completion': '2-3分钟',
                        'trigger_status': trigger_result['message']
                    }
                else:
                    # 如果自动触发失败，提供手动方案
                    response = {
                        'success': True,
                        'message': '⚠️ 自动触发需要配置，请手动触发更新。点击确定后将为您打开GitHub Actions页面...',
                        'status': 'manual_trigger_required',
                        'timestamp': datetime.now().isoformat(),
                        'deployment_type': 'serverless',
                        'update_method': 'manual_github_actions',
                        'manual_url': 'https://github.com/derekguo0/design-news-aggregator/actions/workflows/deploy.yml',
                        'instructions': {
                            'step1': '1. 点击上方链接打开GitHub Actions页面',
                            'step2': '2. 点击"Run workflow"按钮',
                            'step3': '3. 选择main分支并点击"Run workflow"',
                            'step4': '4. 等待2-3分钟后刷新此页面'
                        },
                        'trigger_status': trigger_result['message']
                    }
                    
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
        github_token = os.environ.get('GITHUB_TOKEN')
        repo_name = os.environ.get('GITHUB_REPOSITORY', 'derekguo0/design-news-aggregator')
        
        if github_token:
            try:
                # 触发workflow dispatch
                url = f"https://api.github.com/repos/{repo_name}/actions/workflows/deploy.yml/dispatches"
                headers = {
                    'Authorization': f'token {github_token}',
                    'Accept': 'application/vnd.github.v3+json',
                    'X-GitHub-Api-Version': '2022-11-28'
                }
                data = {'ref': 'main'}
                
                response = requests.post(url, headers=headers, json=data, timeout=10)
                if response.status_code == 204:
                    print("✅ GitHub Actions已成功触发")
                    return {
                        'success': True,
                        'message': 'GitHub Actions workflow 已成功触发'
                    }
                else:
                    print(f"❌ 触发GitHub Actions失败: {response.status_code}, {response.text}")
                    return {
                        'success': False,
                        'message': f'API调用失败: HTTP {response.status_code}'
                    }
            except requests.exceptions.Timeout:
                print("⏰ GitHub API请求超时")
                return {
                    'success': False,
                    'message': 'GitHub API请求超时，请稍后重试'
                }
            except requests.exceptions.ConnectionError:
                print("🌐 网络连接错误")
                return {
                    'success': False,
                    'message': '无法连接到GitHub API，请检查网络连接'
                }
            except Exception as e:
                print(f"💥 触发GitHub Actions异常: {str(e)}")
                return {
                    'success': False,
                    'message': f'请求异常: {str(e)}'
                }
        else:
            print("⚠️ 未配置GITHUB_TOKEN，无法自动触发更新")
            return {
                'success': False,
                'message': '未配置GITHUB_TOKEN环境变量'
            }
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 