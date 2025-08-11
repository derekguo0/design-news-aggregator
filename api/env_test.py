import os
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        # 详细的环境变量诊断
        github_token_raw = os.environ.get('GITHUB_TOKEN')
        github_repo_raw = os.environ.get('GITHUB_REPOSITORY')
        
        # 检查所有包含GITHUB的环境变量
        github_env_vars = {k: v for k, v in os.environ.items() if 'GITHUB' in k.upper()}
        
        # 检查所有环境变量键名（用于发现命名问题）
        all_env_keys = list(os.environ.keys())
        github_related_keys = [k for k in all_env_keys if 'github' in k.lower() or 'token' in k.lower()]
        
        response = {
            'timestamp': datetime.now().isoformat(),
            'environment_diagnosis': {
                'GITHUB_TOKEN_value': github_token_raw,
                'GITHUB_TOKEN_length': len(github_token_raw) if github_token_raw else 0,
                'GITHUB_TOKEN_starts_with_ghp': github_token_raw.startswith('ghp_') if github_token_raw else False,
                'GITHUB_REPOSITORY_value': github_repo_raw,
                'all_github_env_vars': github_env_vars,
                'github_related_keys': github_related_keys,
                'total_env_vars_count': len(all_env_keys)
            },
            'vercel_info': {
                'VERCEL': os.environ.get('VERCEL'),
                'VERCEL_ENV': os.environ.get('VERCEL_ENV'),
                'VERCEL_URL': os.environ.get('VERCEL_URL')
            },
            'debug_suggestions': [
                '1. 检查GITHUB_TOKEN是否真的存在于环境变量中',
                '2. 确认Token格式是否正确（应以ghp_开头）',
                '3. 验证Vercel Environment Variables配置',
                '4. 检查是否有重复或类似的环境变量名'
            ]
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
