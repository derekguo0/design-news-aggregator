#!/usr/bin/env python3
"""
补全归档页面缺失内容的脚本
为缺失的日期创建占位内容并重新生成归档页面
"""

import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Any

def create_placeholder_content(target_date: str) -> Dict[str, Any]:
    """为指定日期创建占位内容"""
    placeholder_data = {
        "date": f"{target_date}T00:00:00",
        "total_items": 0,
        "categories": [],
        "sources": [],
        "generated_at": datetime.now().isoformat(),
        "metadata": {
            "note": f"此日期暂无资讯内容 ({target_date})",
            "status": "placeholder",
            "reason": "历史数据补全"
        }
    }
    return placeholder_data

def create_placeholder_html(target_date: str) -> str:
    """为指定日期创建占位HTML页面"""
    date_obj = datetime.strptime(target_date, '%Y-%m-%d')
    chinese_date = date_obj.strftime('%Y年%m月%d日')
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    chinese_weekday = weekday_names[date_obj.weekday()]
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chinese_date} {chinese_weekday} - Design Drip</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto py-8 px-4">
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">{chinese_date}</h1>
            <p class="text-lg text-gray-600">{chinese_weekday}</p>
        </header>
        
        <div class="bg-white rounded-lg shadow-sm border p-8 text-center">
            <div class="text-6xl mb-4">📰</div>
            <h2 class="text-xl font-semibold text-gray-700 mb-2">暂无资讯内容</h2>
            <p class="text-gray-500 mb-4">此日期的资讯内容正在补充中...</p>
            <div class="text-sm text-gray-400">
                如有需要，请返回 <a href="/" class="text-blue-500 hover:underline">首页</a> 
                或查看 <a href="/archive.html" class="text-blue-500 hover:underline">归档页面</a>
            </div>
        </div>
        
        <div class="mt-8 text-center">
            <a href="/archive.html" class="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                ← 返回归档页面
            </a>
        </div>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    """主函数：补全缺失的日期内容"""
    print("🔧 开始补全归档页面缺失内容...")
    
    # 缺失的日期列表
    missing_dates = [
        "2025-07-27",
        "2025-07-29", 
        "2025-08-02",
        "2025-08-03",
        "2025-08-04",
        "2025-08-05"
    ]
    
    data_dir = Path("data")
    output_dir = Path("output")
    
    # 创建目录（如果不存在）
    data_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    created_files = []
    
    for date_str in missing_dates:
        print(f"📅 处理日期: {date_str}")
        
        # 创建数据文件
        json_filename = f"digest-{date_str}.json"
        json_path = data_dir / json_filename
        
        if not json_path.exists():
            placeholder_data = create_placeholder_content(date_str)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(placeholder_data, f, ensure_ascii=False, indent=2)
            print(f"  ✅ 创建数据文件: {json_filename}")
            created_files.append(json_filename)
        else:
            print(f"  ⏭️  数据文件已存在: {json_filename}")
        
        # 创建HTML页面
        html_filename = f"daily-{date_str}.html"
        html_path = output_dir / html_filename
        
        if not html_path.exists():
            placeholder_html = create_placeholder_html(date_str)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(placeholder_html)
            print(f"  ✅ 创建页面文件: {html_filename}")
            created_files.append(html_filename)
        else:
            print(f"  ⏭️  页面文件已存在: {html_filename}")
    
    print(f"\n🎉 补全完成！共创建了 {len(created_files)} 个文件")
    print("\n📋 创建的文件列表：")
    for filename in created_files:
        print(f"  - {filename}")
    
    print(f"\n📊 现在请运行生成脚本来更新归档页面：")
    print("  python3 simple_run.py")

if __name__ == "__main__":
    main()