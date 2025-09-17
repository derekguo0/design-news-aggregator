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
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_response = {
                "success": False,
                "ok": False,
                "message": f"快速刷新失败: {str(e)}",
                "status": "quick_refresh_failed",
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
    
    def _quick_content_generation(self):
        """快速内容生成 - 适合serverless环境"""
        try:
            # 创建必要目录
            output_dir = project_root / "output"
            data_dir = project_root / "data"
            output_dir.mkdir(exist_ok=True)
            data_dir.mkdir(exist_ok=True)
            
            # 生成今日内容
            today = datetime.now().strftime('%Y-%m-%d')
            time_str = datetime.now().strftime('%H:%M:%S')
            
            # 创建测试数据
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
            
            # 保存数据文件
            with open(data_dir / f"digest-{today}.json", 'w', encoding='utf-8') as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2)
            
            # 生成HTML页面
            html_content = self._generate_html_page(test_data, today)
            
            # 保存HTML文件
            with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            with open(output_dir / f"daily-{today}.html", 'w', encoding='utf-8') as f:
                f.write(html_content.replace("设计资讯聚合", f"设计资讯聚合 - {today}"))
            
            return {
                "files_generated": [
                    f"data/digest-{today}.json",
                    "output/index.html", 
                    f"output/daily-{today}.html"
                ],
                "items_count": 8,
                "generation_time": time_str,
                "refresh_type": "quick_test"
            }
            
        except Exception as e:
            raise Exception(f"快速内容生成失败: {str(e)}")
    
    def _generate_html_page(self, data, today):
        """生成HTML页面"""
        items_html = ""
        for category in data['categories']:
            for item in category['items']:
                items_html += f'''
                <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                    <h3 class="text-lg font-semibold text-gray-900 mb-2">
                        <a href="{item['url']}" target="_blank" class="hover:text-blue-600">
                            {item['title']}
                        </a>
                    </h3>
                    <p class="text-gray-600 mb-4">{item['summary']}</p>
                    <div class="flex justify-between items-center text-sm text-gray-500">
                        <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded">{item['category']}</span>
                        <span>{item['source']}</span>
                    </div>
                </div>
                '''
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>设计资讯聚合 - {today}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto py-8 px-4">
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">设计资讯聚合</h1>
            <p class="text-gray-600">最新的设计趋势和资讯 - {today}</p>
            <div class="mt-4">
                <button onclick="window.location.reload()" 
                        class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    🔄 刷新页面
                </button>
            </div>
        </header>
        
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
            <strong>✅ 快速刷新成功！</strong> 内容已更新于 {datetime.now().strftime('%H:%M:%S')}
        </div>
        
        <div class="grid gap-6 md:grid-cols-1 lg:grid-cols-1">
            {items_html}
        </div>
        
        <footer class="text-center mt-8 text-gray-500">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>共 {data['total_items']} 条资讯</p>
            <p class="text-sm text-gray-400 mt-2">快速刷新模式 - 生成测试内容</p>
        </footer>
    </div>
</body>
</html>'''
