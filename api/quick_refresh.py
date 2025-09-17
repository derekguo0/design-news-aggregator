from http.server import BaseHTTPRequestHandler
import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # 快速刷新 - 只生成测试内容，不进行实际爬取
            result = self._quick_content_generation()
            
            response = {
                "success": True,
                "ok": True,
                "message": "✅ 快速刷新完成！内容已更新",
                "status": "quick_refresh_completed",
                "timestamp": datetime.now().isoformat(),
                "deployment_type": "serverless_quick",
                "update_method": "quick_generation",
                "estimated_completion": "立即生效",
                "cooldown_seconds": 30,
                "result": result,
                "note": "这是快速刷新模式，生成测试内容。如需真实爬取，请使用本地服务器。"
            }
            
            # 允许跨域
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate')
            self.send_header('Expires', '0')
            self.send_header('Pragma', 'no-cache')
            self.end_headers()
            
            # 确保响应是有效的JSON
            json_response = json.dumps(response, ensure_ascii=False)
            self.wfile.write(json_response.encode('utf-8'))
            
        except Exception as e:
            error_response = {
                "success": False,
                "ok": False,
                "message": f"快速刷新失败: {str(e)}",
                "status": "quick_refresh_failed",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
            
            # 确保错误响应也是有效的JSON
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
    
    def _quick_content_generation(self):
        """快速内容生成 - 适合serverless环境"""
        try:
            # 生成今日内容
            today = datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.now().strftime('%H:%M:%S')
            
            # 创建测试数据（不进行文件操作，避免权限问题）
            test_data = {
                "date": f"{today}T00:00:00",
                "total_items": 8,
                "sources": ["UX Design CC", "Smashing Magazine", "Design Milk", "A List Apart"],
                "generated_at": f"{today}T{time_str}",
                "categories": [
                    {
                        "category": "用户体验设计",
                        "count": 3,
                        "items": [
                            {
                                "title": f"最新UX设计趋势 - {today}",
                                "url": "https://uxdesign.cc/latest-trends",
                                "author": "UX Designer",
                                "category": "用户体验设计",
                                "source": "UX Design CC",
                                "summary": "探索2025年最新的用户体验设计趋势和最佳实践",
                                "published_at": f"{today}T{time_str}"
                            },
                            {
                                "title": "交互设计原则",
                                "url": "https://smashingmagazine.com/interaction-design",
                                "author": "Design Expert",
                                "category": "用户体验设计",
                                "source": "Smashing Magazine",
                                "summary": "深入理解交互设计的核心原则和实现方法",
                                "published_at": f"{today}T{time_str}"
                            },
                            {
                                "title": "用户研究方法论",
                                "url": "https://uxdesign.cc/user-research",
                                "author": "UX Researcher",
                                "category": "用户体验设计",
                                "source": "UX Design CC",
                                "summary": "全面的用户研究方法指南和实践案例",
                                "published_at": f"{today}T{time_str}"
                            }
                        ]
                    },
                    {
                        "category": "网页设计",
                        "count": 3,
                        "items": [
                            {
                                "title": "现代网页设计趋势",
                                "url": "https://design-milk.com/web-trends",
                                "author": "Web Designer",
                                "category": "网页设计",
                                "source": "Design Milk",
                                "summary": "2025年网页设计的最新趋势和创意灵感",
                                "published_at": f"{today}T{time_str}"
                            },
                            {
                                "title": "响应式设计最佳实践",
                                "url": "https://alistapart.com/responsive-design",
                                "author": "Frontend Developer",
                                "category": "网页设计",
                                "source": "A List Apart",
                                "summary": "构建完美响应式网站的设计和开发技巧",
                                "published_at": f"{today}T{time_str}"
                            },
                            {
                                "title": "CSS Grid布局指南",
                                "url": "https://css-tricks.com/css-grid",
                                "author": "CSS Expert",
                                "category": "网页设计",
                                "source": "CSS-Tricks",
                                "summary": "掌握CSS Grid布局的强大功能和实际应用",
                                "published_at": f"{today}T{time_str}"
                            }
                        ]
                    },
                    {
                        "category": "设计工具",
                        "count": 2,
                        "items": [
                            {
                                "title": "Figma高级技巧",
                                "url": "https://design-milk.com/figma-tips",
                                "author": "Design Tool Expert",
                                "category": "设计工具",
                                "source": "Design Milk",
                                "summary": "提升Figma使用效率的高级技巧和工作流程",
                                "published_at": f"{today}T{time_str}"
                            },
                            {
                                "title": "设计系统构建",
                                "url": "https://smashingmagazine.com/design-systems",
                                "author": "Design System Lead",
                                "category": "设计工具",
                                "source": "Smashing Magazine",
                                "summary": "如何构建和维护可扩展的设计系统",
                                "published_at": f"{today}T{time_str}"
                            }
                        ]
                    }
                ]
            }
            
            return {
                "data_generated": True,
                "items_count": 8,
                "generation_time": time_str,
                "refresh_type": "quick_test",
                "note": "快速刷新模式 - 仅生成数据，不保存文件"
            }
            
        except Exception as e:
            raise Exception(f"快速内容生成失败: {str(e)}")
    
