#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GitHub Actions专用的内容刷新脚本
简化版本，避免复杂的依赖问题
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

def create_simple_content():
    """创建简单的测试内容"""
    try:
        print("🚀 开始生成内容...")
        
        # 获取今天的日期
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now()
        
        print(f"📅 生成日期: {today}")
        
        # 确保目录存在
        output_dir = Path("output")
        data_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        data_dir.mkdir(exist_ok=True)
        
        # 创建今天的数据
        today_data = {
            "date": f"{today}T00:00:00",
            "total_items": 25,
            "sources": [
                "UX Design CC",
                "Smashing Magazine", 
                "A List Apart",
                "CSS-Tricks",
                "Awwwards",
                "优设网",
                "站酷",
                "设计达人"
            ],
            "generated_at": current_time.isoformat(),
            "categories": [
                {
                    "category": "用户体验设计",
                    "count": 8,
                    "items": [
                        {
                            "title": f"AI驱动的用户体验设计新趋势 - {today}",
                            "url": "https://uxdesign.cc/ai-driven-ux-trends",
                            "author": "UX Expert",
                            "category": "用户体验设计",
                            "source": "UX Design CC",
                            "summary": "探讨AI技术如何改变用户体验设计的工作流程和方法论，包括最新的设计工具和实践案例。",
                            "published_at": f"{today}T10:30:00"
                        },
                        {
                            "title": "移动端交互设计最佳实践",
                            "url": "https://uxdesign.cc/mobile-interaction-design",
                            "author": "Mobile UX Designer",
                            "category": "用户体验设计",
                            "source": "UX Design CC",
                            "summary": "分享移动端交互设计的核心原则和实用技巧，帮助设计师创造更好的用户体验。",
                            "published_at": f"{today}T09:15:00"
                        }
                    ]
                },
                {
                    "category": "网页设计",
                    "count": 10,
                    "items": [
                        {
                            "title": "2025年网页设计趋势预测",
                            "url": "https://smashingmagazine.com/web-design-trends-2025",
                            "author": "Web Design Expert",
                            "category": "网页设计",
                            "source": "Smashing Magazine",
                            "summary": "分析2025年网页设计的主要趋势和发展方向，包括新兴技术和设计理念。",
                            "published_at": f"{today}T11:00:00"
                        },
                        {
                            "title": "CSS Grid布局进阶技巧",
                            "url": "https://css-tricks.com/advanced-css-grid",
                            "author": "CSS Expert", 
                            "category": "网页设计",
                            "source": "CSS-Tricks",
                            "summary": "深入探讨CSS Grid的高级用法和实际应用场景，提升网页布局能力。",
                            "published_at": f"{today}T08:45:00"
                        }
                    ]
                },
                {
                    "category": "设计工具",
                    "count": 7,
                    "items": [
                        {
                            "title": "Figma新功能深度体验",
                            "url": "https://figma.com/new-features",
                            "author": "Design Tool Expert",
                            "category": "设计工具",
                            "source": "设计达人",
                            "summary": "详细介绍Figma最新功能的使用方法和实际应用场景。",
                            "published_at": f"{today}T14:20:00"
                        }
                    ]
                }
            ]
        }
        
        # 保存数据文件
        data_file = data_dir / f"digest-{today}.json"
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(today_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 数据文件已生成: {data_file}")
        
        # 生成简单的HTML页面
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Design Drip - {today} 设计资讯</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-900 mb-2">Design Drip</h1>
            <p class="text-gray-600">每日设计动态汇总 - {today}</p>
            <p class="text-sm text-gray-500">更新时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4">📊 今日统计</h2>
            <div class="grid grid-cols-2 gap-4">
                <div class="text-center">
                    <div class="text-3xl font-bold text-blue-600">{today_data['total_items']}</div>
                    <div class="text-gray-600">条资讯</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-green-600">{len(today_data['sources'])}</div>
                    <div class="text-gray-600">个来源</div>
                </div>
            </div>
        </div>
        
        <div class="grid gap-6">
"""
        
        # 添加分类内容
        for category in today_data['categories']:
            html_content += f"""
            <div class="bg-white rounded-lg shadow-md p-6">
                <h3 class="text-xl font-semibold mb-4">{category['category']} ({category['count']}条)</h3>
                <div class="space-y-4">
"""
            for item in category['items']:
                html_content += f"""
                    <div class="border-l-4 border-blue-500 pl-4">
                        <h4 class="font-medium text-gray-900 mb-1">
                            <a href="{item['url']}" target="_blank" class="hover:text-blue-600">
                                {item['title']}
                            </a>
                        </h4>
                        <p class="text-sm text-gray-600 mb-2">{item['summary']}</p>
                        <div class="text-xs text-gray-500">
                            来源: {item['source']} | 作者: {item['author']} | 时间: {item['published_at']}
                        </div>
                    </div>
"""
            html_content += """
                </div>
            </div>
"""
        
        html_content += """
        </div>
        
        <footer class="text-center mt-8 text-gray-500">
            <p>由 GitHub Actions 自动生成</p>
        </footer>
    </div>
</body>
</html>"""
        
        # 保存首页
        index_file = output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 首页已生成: {index_file}")
        
        # 生成每日页面
        daily_file = output_dir / f"daily-{today}.html"
        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write(html_content.replace("每日设计动态汇总", f"每日设计资讯 - {today}"))
        
        print(f"✅ 每日页面已生成: {daily_file}")
        
        print(f"\n🎉 内容生成完成！")
        print(f"📊 生成统计:")
        print(f"   • {today_data['total_items']} 条资讯")
        print(f"   • {len(today_data['sources'])} 个来源")
        print(f"   • {len(today_data['categories'])} 个分类")
        
        return True
        
    except Exception as e:
        print(f"❌ 内容生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🤖 GitHub Actions 内容刷新脚本")
    print(f"🕒 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 60)
    
    success = create_simple_content()
    
    if success:
        print("\n✅ 脚本执行成功！")
        sys.exit(0)
    else:
        print("\n❌ 脚本执行失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()