#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
修复首页脚本
重新生成首页，确保使用今天的最新数据
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.generators.web_generator import WebGenerator
from src.models import DailyDigest

def fix_homepage():
    """修复首页，确保使用今天的最新数据"""
    try:
        print("🔧 开始修复首页...")
        
        # 创建网页生成器
        generator = WebGenerator()
        
        # 加载今天的数据
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"📅 加载今天的数据: {today}")
        
        digest = generator.load_daily_digest(today)
        if not digest:
            print(f"❌ 未找到今天的数据文件: digest-{today}.json")
            return False
        
        print(f"✅ 成功加载今天的数据: {digest.total_items} 条资讯")
        
        # 加载所有历史数据
        all_digests = generator.load_all_digests()
        print(f"📚 加载了 {len(all_digests)} 个历史摘要")
        
        # 确保今天的数据在首位
        if all_digests and all_digests[0].date.date() != digest.date.date():
            # 移除可能存在的重复项
            all_digests = [d for d in all_digests if d.date.date() != digest.date.date()]
            # 在开头插入今天的数据
            all_digests.insert(0, digest)
            print("🔄 已将今天的数据置于首位")
        
        # 使用最近7天的数据生成首页
        recent_digests = all_digests[:7]
        print(f"📊 使用最近 {len(recent_digests)} 天的数据生成首页")
        
        # 重新生成首页
        print("🔄 重新生成首页...")
        index_path = generator.generate_index_page(recent_digests)
        print(f"✅ 首页生成成功: {index_path}")
        
        # 重新生成归档页
        print("🔄 重新生成归档页...")
        archive_path = generator.generate_archive_page(all_digests)
        print(f"✅ 归档页生成成功: {archive_path}")
        
        # 重新生成RSS
        print("🔄 重新生成RSS...")
        rss_path = generator.generate_rss_feed(recent_digests)
        print(f"✅ RSS生成成功: {rss_path}")
        
        # 重新生成sitemap
        print("🔄 重新生成sitemap...")
        sitemap_path = generator.generate_sitemap(all_digests)
        print(f"✅ Sitemap生成成功: {sitemap_path}")
        
        print("\n🎉 首页修复完成！")
        print("📄 生成的文件:")
        print(f"   • {index_path}")
        print(f"   • {archive_path}")
        print(f"   • {rss_path}")
        print(f"   • {sitemap_path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 修复失败: {e}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = fix_homepage()
    sys.exit(0 if success else 1)
