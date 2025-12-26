"""
诊断脚本：检查所有资讯来源的抓取状态
"""
import json
import sys
from pathlib import Path
from loguru import logger
from src.config import get_config
from src.crawlers.base import create_crawler

def check_all_sources():
    """检查所有来源"""
    logger.info("开始检查所有资讯来源...")
    
    # 加载配置
    config = get_config()
    sources = config.sources
    
    results = {
        "total": len(sources),
        "enabled": 0,
        "disabled": 0,
        "success": [],
        "failed": [],
        "empty": []
    }
    
    for source in sources:
        if not source.enabled:
            results["disabled"] += 1
            logger.warning(f"❌ {source.name} - 已禁用")
            continue
        
        results["enabled"] += 1
        
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"正在检查: {source.name}")
            logger.info(f"类型: {source.type}")
            logger.info(f"URL: {source.url}")
            logger.info(f"分类: {source.category}")
            
            # 创建爬虫并抓取
            crawler = create_crawler(source)
            items = crawler.crawl()
            
            if items:
                logger.success(f"✅ {source.name} - 成功抓取 {len(items)} 条")
                results["success"].append({
                    "name": source.name,
                    "type": source.type,
                    "count": len(items),
                    "category": source.category
                })
                
                # 显示前3条标题
                for i, item in enumerate(items[:3], 1):
                    logger.info(f"  {i}. {item.title}")
            else:
                logger.warning(f"⚠️  {source.name} - 未抓取到任何内容")
                results["empty"].append({
                    "name": source.name,
                    "type": source.type,
                    "url": source.url,
                    "category": source.category
                })
                
        except Exception as e:
            logger.error(f"❌ {source.name} - 抓取失败: {e}")
            results["failed"].append({
                "name": source.name,
                "type": source.type,
                "url": source.url,
                "category": source.category,
                "error": str(e)
            })
    
    # 打印总结
    print("\n" + "="*60)
    print("📊 检查结果汇总")
    print("="*60)
    print(f"总来源数: {results['total']}")
    print(f"已启用: {results['enabled']}")
    print(f"已禁用: {results['disabled']}")
    print(f"✅ 成功抓取: {len(results['success'])}")
    print(f"⚠️  抓取为空: {len(results['empty'])}")
    print(f"❌ 抓取失败: {len(results['failed'])}")
    
    if results['success']:
        print("\n✅ 成功抓取的来源:")
        for item in results['success']:
            print(f"  - {item['name']} ({item['type']}): {item['count']} 条 - {item['category']}")
    
    if results['empty']:
        print("\n⚠️  抓取为空的来源 (可能需要更新选择器):")
        for item in results['empty']:
            print(f"  - {item['name']} ({item['type']}) - {item['category']}")
            print(f"    URL: {item['url']}")
    
    if results['failed']:
        print("\n❌ 抓取失败的来源:")
        for item in results['failed']:
            print(f"  - {item['name']} ({item['type']}) - {item['category']}")
            print(f"    URL: {item['url']}")
            print(f"    错误: {item['error']}")
    
    # 保存详细报告
    report_path = Path(__file__).parent / "source_check_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存至: {report_path}")
    
    return results

if __name__ == "__main__":
    check_all_sources()

