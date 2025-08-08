from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # 收集环境信息
            debug_info = {
                'timestamp': datetime.now().isoformat(),
                'environment': {
                    'VERCEL': os.environ.get('VERCEL', 'Not set'),
                    'VERCEL_ENV': os.environ.get('VERCEL_ENV', 'Not set'),
                    'GITHUB_TOKEN': 'Configured' if os.environ.get('GITHUB_TOKEN') else 'Not configured',
                    'GITHUB_REPOSITORY': os.environ.get('GITHUB_REPOSITORY', 'Not set')
                },
                'deployment_detection': {
                    'is_vercel': bool(os.environ.get('VERCEL')) or bool(os.environ.get('VERCEL_ENV')),
                    'has_github_token': bool(os.environ.get('GITHUB_TOKEN'))
                },
                'status': 'API is responding normally',
                'debug_tips': {
                    'refresh_not_working': [
                        '1. 检查网络连接是否正常',
                        '2. 确认是否在Vercel环境中部署',
                        '3. 验证GITHUB_TOKEN是否已配置',
                        '4. 查看浏览器控制台的错误信息',
                        '5. 尝试手动触发GitHub Actions'
                    ],
                    'manual_github_actions': 'https://github.com/derekguo0/design-news-aggregator/actions/workflows/deploy.yml'
                }
            }
            
            self.wfile.write(json.dumps(debug_info, ensure_ascii=False, indent=2).encode('utf-8'))
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'success': False,
                'message': f'调试API错误: {str(e)}',
                'status': 'error'
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
