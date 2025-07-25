from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import sys
import os
import subprocess

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # 立即返回开始响应
            response = {
                'success': True,
                'message': '刷新任务已启动，正在后台执行...',
                'status': 'started',
                'timestamp': datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
            # 在后台执行刷新任务
            try:
                # 获取项目根目录
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                
                # 执行刷新脚本（设置较短的超时时间）
                result = subprocess.run([
                    sys.executable, 
                    os.path.join(project_root, 'simple_run.py')
                ], 
                cwd=project_root,
                capture_output=True, 
                text=True, 
                timeout=240  # 4分钟超时
                )
                
                # 由于HTTP响应已发送，这里的结果不会返回给客户端
                # 但会在服务器日志中记录
                if result.returncode == 0:
                    print(f"✅ 刷新成功完成: {datetime.now().isoformat()}")
                else:
                    print(f"❌ 刷新失败: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"⏰ 刷新超时: {datetime.now().isoformat()}")
            except Exception as e:
                print(f"💥 刷新异常: {str(e)}")
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            response = {
                'success': False,
                'message': f'启动刷新任务失败: {str(e)}',
                'status': 'error'
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 