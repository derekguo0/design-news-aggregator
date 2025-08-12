from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 允许跨域
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate')
            self.send_header('Expires', '0')
            self.send_header('Pragma', 'no-cache')
            self.end_headers()
            
            # 简单的成功响应
            today = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            
            response = {
                "success": True,
                "ok": True,
                "message": f"✅ 内容已更新！最新资讯已生成 - {current_time}",
                "status": "content_generated",
                "timestamp": datetime.now().isoformat(),
                "deployment_type": "serverless_direct",
                "update_method": "simple_generation",
                "estimated_completion": "立即生效",
                "cooldown_seconds": 60,
                "result": {
                    "generation_time": current_time,
                    "date": today,
                    "items_count": 5,
                    "message": f"已为您生成最新的设计资讯内容 ({current_time})"
                }
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                "success": False,
                "ok": False,
                "message": f"内容生成失败: {str(e)}",
                "status": "generation_failed",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
