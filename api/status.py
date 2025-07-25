from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # 返回系统状态
        response = {
            'is_running': False,  # Serverless无法跟踪长期状态
            'last_refresh': datetime.now().isoformat(),
            'error': None,
            'deployment_type': 'serverless',
            'message': 'Serverless环境运行中',
            'timestamp': datetime.now().isoformat(),
            'status': 'ready'
        }
        
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 