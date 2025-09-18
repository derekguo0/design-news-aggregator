#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
重新生成首页脚本
直接重新生成首页，确保使用今天的最新数据
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def regenerate_homepage():
    """重新生成首页"""
    try:
        print("🔧 开始重新生成首页...")
        
        # 加载今天的数据
        today = datetime.now().strftime('%Y-%m-%d')
        data_file = project_root / "data" / f"digest-{today}.json"
        
        if not data_file.exists():
            print(f"❌ 未找到今天的数据文件: {data_file}")
            return False
        
        print(f"📅 加载今天的数据: {today}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            today_data = json.load(f)
        
        print(f"✅ 成功加载今天的数据: {today_data['total_items']} 条资讯")
        
        # 加载所有历史数据
        data_dir = project_root / "data"
        all_digests = []
        
        for file_path in data_dir.glob("digest-*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    digest_data = json.load(f)
                all_digests.append(digest_data)
            except Exception as e:
                print(f"⚠️ 跳过文件 {file_path}: {e}")
                continue
        
        # 按日期排序（最新的在前）
        all_digests.sort(key=lambda x: x['date'], reverse=True)
        print(f"📚 加载了 {len(all_digests)} 个历史摘要")
        
        # 使用最近7天的数据
        recent_digests = all_digests[:7]
        print(f"📊 使用最近 {len(recent_digests)} 天的数据")
        
        # 计算统计信息
        total_items = sum(digest['total_items'] for digest in recent_digests)
        all_sources = set()
        for digest in recent_digests:
            all_sources.update(digest['sources'])
        
        print(f"📈 统计信息: {total_items} 条资讯, {len(all_sources)} 个来源")
        
        # 读取首页模板
        template_file = project_root / "templates" / "index.html"
        if not template_file.exists():
            print(f"❌ 未找到首页模板: {template_file}")
            return False
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 更新统计信息
        template_content = template_content.replace(
            f'已收集{113}条来自{11}个优质设计网站的资讯',
            f'已收集{total_items}条来自{len(all_sources)}个优质设计网站的资讯'
        )
        
        # 更新最后更新时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        template_content = template_content.replace(
            '最后更新: 2025-09-17 14:05',
            f'最后更新: {current_time}'
        )
        
        # 保存更新后的首页
        output_file = project_root / "output" / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✅ 首页更新成功: {output_file}")
        print(f"📊 更新统计: {total_items} 条资讯, {len(all_sources)} 个来源")
        print(f"🕐 更新时间: {current_time}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 更新失败: {e}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = regenerate_homepage()
    sys.exit(0 if success else 1)
