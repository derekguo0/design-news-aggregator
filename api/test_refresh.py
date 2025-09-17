from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 简单的测试响应
            response = {
                "success": True,
                "ok": True,
                "message": "✅ 测试刷新成功！",
                "status": "test_success",
                "timestamp": datetime.now().isoformat(),
                "deployment_type": "serverless_test",
                "update_method": "test_generation",
                "estimated_completion": "立即生效",
                "cooldown_seconds": 10,
                "result": {
                    "test": True,
                    "items_count": 5,
                    "generation_time": datetime.now().strftime('%H:%M:%S')
                }
            }
            
            # 设置响应头
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            
            # 发送JSON响应
            json_response = json.dumps(response, ensure_ascii=False)
            self.wfile.write(json_response.encode('utf-8'))
            
        except Exception as e:
            error_response = {
                "success": False,
                "ok": False,
                "message": f"测试失败: {str(e)}",
                "status": "test_failed",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            
            self.send_response(500)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            
            json_error = json.dumps(error_response, ensure_ascii=False)
            self.wfile.write(json_error.encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
