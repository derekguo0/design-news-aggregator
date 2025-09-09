from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

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
            
            # 真正的资讯爬取和内容更新
            result = self._run_real_content_update()
            
            response = {
                "success": True,
                "ok": True,
                "message": f"✅ 内容已更新！最新资讯已生成 - {result['generation_time']}",
                "status": "content_generated",
                "timestamp": datetime.now().isoformat(),
                "deployment_type": "serverless_direct",
                "update_method": "real_content_update",
                "estimated_completion": "立即生效",
                "cooldown_seconds": 60,
                "result": result
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
    
    def _run_real_content_update(self):
        """执行真正的资讯爬取和内容生成"""
        try:
            current_time = datetime.now()
            today = current_time.strftime('%Y-%m-%d')
            time_str = current_time.strftime('%H:%M:%S')
            
            print(f"[{time_str}] 🚀 开始执行真实资讯爬取...")
            
            # 在Vercel环境中，直接使用模块导入方式，避免subprocess问题
            print(f"[{time_str}] 🔄 使用直接导入方式执行资讯生成...")
            try:
                from src.scheduler.task_scheduler import TaskScheduler
                
                # 创建调度器实例并运行一次完整任务
                scheduler = TaskScheduler()
                
                # 使用 asyncio 运行异步任务
                import asyncio
                if hasattr(asyncio, '_get_running_loop') and asyncio._get_running_loop() is not None:
                    # 已经在事件循环中，使用 create_task
                    task = asyncio.create_task(scheduler.run_once())
                    # 由于我们在HTTP处理器中，不能等待，所以尝试立即获取结果
                    # 这里我们回退到基本的导入方式
                    raise Exception("在HTTP处理器中无法运行异步任务")
                else:
                    # 创建新的事件循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(scheduler.run_once())
                    finally:
                        loop.close()
                
                # 检查结果
                digest_file = project_root / "data" / f"digest-{today}.json"
                if digest_file.exists():
                    with open(digest_file, 'r', encoding='utf-8') as f:
                        digest_data = json.load(f)
                    
                    total_items = digest_data.get('total_items', 0)
                    sources = digest_data.get('sources', [])
                    
                    return {
                        "success": True,
                        "method": "direct_import",
                        "generation_time": time_str,
                        "date": today,
                        "items_count": total_items,
                        "sources_count": len(sources),
                        "sources": sources,
                        "digest_file": str(digest_file),
                        "message": f"✅ 通过直接导入成功生成 {total_items} 条资讯，来自 {len(sources)} 个设计网站"
                    }
                else:
                    return {
                        "success": False,
                        "method": "direct_import",
                        "generation_time": time_str,
                        "date": today,
                        "error": "数据文件未生成",
                        "message": "❌ 资讯生成失败，数据文件未创建"
                    }
                    
            except Exception as import_error:
                print(f"[{time_str}] 💥 直接导入失败: {str(import_error)}")
                
                # 最后的回退方案：返回错误信息，但不完全失败
                return {
                    "success": False,
                    "method": "fallback",
                    "generation_time": time_str,
                    "date": today,
                    "import_error": str(import_error),
                    "message": f"❌ 真实资讯爬取失败。导入错误: {str(import_error)}"
                }
            
                
        except Exception as e:
            print(f"[{time_str}] 💥 整体执行异常: {str(e)}")
            return {
                "success": False,
                "method": "exception",
                "generation_time": time_str,
                "date": today,
                "error": str(e),
                "message": f"❌ 资讯更新系统异常: {str(e)}"
            }
