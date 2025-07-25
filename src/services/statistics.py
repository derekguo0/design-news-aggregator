#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
统计服务模块
提供数据统计和分析结果展示功能
"""

import json
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class StatisticsService:
    """统计服务类"""
    
    def __init__(self):
        self.data_dir = "data"
        self.feeds_file = os.path.join(self.data_dir, "feeds_data.json")
        self.ai_analysis_file = os.path.join(self.data_dir, "ai_analysis.json")
        
    def load_feeds_data(self) -> Dict:
        """加载RSS数据"""
        try:
            if os.path.exists(self.feeds_file):
                with open(self.feeds_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载RSS数据失败: {e}")
        return {}
    
    def load_ai_analysis(self) -> Dict:
        """加载AI分析数据"""
        try:
            if os.path.exists(self.ai_analysis_file):
                with open(self.ai_analysis_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载AI分析数据失败: {e}")
        return {}
    
    def get_basic_statistics(self) -> Dict[str, Any]:
        """获取基础统计信息"""
        feeds_data = self.load_feeds_data()
        ai_analysis = self.load_ai_analysis()
        
        stats = {
            'total_sources': 0,
            'total_articles': 0,
            'articles_with_ai': 0,
            'ai_success_rate': 0,
            'sources_stats': {},
            'update_time': None
        }
        
        if not feeds_data:
            return stats
        
        # 基础统计
        stats['total_sources'] = len(feeds_data.get('sources', {}))
        
        articles_count = 0
        ai_count = 0
        sources_stats = {}
        
        for source_name, source_data in feeds_data.get('sources', {}).items():
            items = source_data.get('items', [])
            articles_count += len(items)
            
            # 统计该源的AI分析数量
            ai_items = sum(1 for item in items if item.get('link') in ai_analysis)
            ai_count += ai_items
            
            sources_stats[source_name] = {
                'total_articles': len(items),
                'ai_analyzed': ai_items,
                'success_rate': (ai_items / len(items) * 100) if items else 0
            }
        
        stats['total_articles'] = articles_count
        stats['articles_with_ai'] = ai_count
        stats['ai_success_rate'] = (ai_count / articles_count * 100) if articles_count > 0 else 0
        stats['sources_stats'] = sources_stats
        stats['update_time'] = feeds_data.get('generated_at')
        
        return stats
    
    def get_content_analysis(self) -> Dict[str, Any]:
        """获取内容分析统计"""
        ai_analysis = self.load_ai_analysis()
        
        if not ai_analysis:
            return {}
        
        # 分析摘要长度分布
        summary_lengths = [len(data.get('summary', '')) for data in ai_analysis.values()]
        
        # 分析关键词频率（简单的词频统计）
        all_summaries = ' '.join([data.get('summary', '') for data in ai_analysis.values()])
        
        analysis = {
            'total_summaries': len(ai_analysis),
            'avg_summary_length': sum(summary_lengths) / len(summary_lengths) if summary_lengths else 0,
            'min_summary_length': min(summary_lengths) if summary_lengths else 0,
            'max_summary_length': max(summary_lengths) if summary_lengths else 0,
            'summary_length_distribution': self._get_length_distribution(summary_lengths)
        }
        
        return analysis
    
    def _get_length_distribution(self, lengths: List[int]) -> Dict[str, int]:
        """获取长度分布"""
        distribution = {
            'very_short': 0,  # < 50字符
            'short': 0,       # 50-100字符
            'medium': 0,      # 100-200字符
            'long': 0,        # 200-300字符
            'very_long': 0    # > 300字符
        }
        
        for length in lengths:
            if length < 50:
                distribution['very_short'] += 1
            elif length < 100:
                distribution['short'] += 1
            elif length < 200:
                distribution['medium'] += 1
            elif length < 300:
                distribution['long'] += 1
            else:
                distribution['very_long'] += 1
        
        return distribution
    
    def get_time_analysis(self) -> Dict[str, Any]:
        """获取时间分析统计"""
        feeds_data = self.load_feeds_data()
        
        if not feeds_data:
            return {}
        
        # 收集所有文章的发布时间
        articles_by_hour = defaultdict(int)
        articles_by_day = defaultdict(int)
        recent_articles = 0
        
        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        
        for source_data in feeds_data.get('sources', {}).values():
            for item in source_data.get('items', []):
                pub_date = item.get('published_parsed')
                if pub_date:
                    try:
                        # 转换为datetime对象
                        dt = datetime(*pub_date[:6])
                        hour = dt.hour
                        day = dt.strftime('%Y-%m-%d')
                        
                        articles_by_hour[hour] += 1
                        articles_by_day[day] += 1
                        
                        # 统计最近24小时的文章
                        if dt > one_day_ago:
                            recent_articles += 1
                            
                    except Exception:
                        continue
        
        # 找出最活跃的时间段
        peak_hour = max(articles_by_hour.items(), key=lambda x: x[1]) if articles_by_hour else (0, 0)
        
        return {
            'articles_by_hour': dict(articles_by_hour),
            'articles_by_day': dict(articles_by_day),
            'peak_hour': peak_hour[0],
            'peak_hour_count': peak_hour[1],
            'recent_articles_24h': recent_articles,
            'total_days_covered': len(articles_by_day)
        }
    
    def generate_report(self) -> str:
        """生成统计报告"""
        basic_stats = self.get_basic_statistics()
        content_stats = self.get_content_analysis()
        time_stats = self.get_time_analysis()
        
        report = []
        report.append("📊 推送机器人统计报告")
        report.append("=" * 50)
        
        # 基础统计
        report.append(f"\n🔢 基础统计:")
        report.append(f"  • RSS源数量: {basic_stats['total_sources']}")
        report.append(f"  • 文章总数: {basic_stats['total_articles']}")
        report.append(f"  • AI分析数量: {basic_stats['articles_with_ai']}")
        report.append(f"  • AI成功率: {basic_stats['ai_success_rate']:.1f}%")
        
        if basic_stats['update_time']:
            report.append(f"  • 最后更新: {basic_stats['update_time']}")
        
        # 各源统计
        if basic_stats['sources_stats']:
            report.append(f"\n📈 各RSS源统计:")
            for source, stats in basic_stats['sources_stats'].items():
                report.append(f"  • {source}: {stats['total_articles']}篇文章, "
                            f"AI分析 {stats['ai_analyzed']}篇 ({stats['success_rate']:.1f}%)")
        
        # 内容分析
        if content_stats:
            report.append(f"\n📝 内容分析:")
            report.append(f"  • 平均摘要长度: {content_stats['avg_summary_length']:.1f}字符")
            report.append(f"  • 摘要长度范围: {content_stats['min_summary_length']}-{content_stats['max_summary_length']}字符")
            
            dist = content_stats['summary_length_distribution']
            report.append(f"  • 长度分布: 很短({dist['very_short']}) | "
                        f"短({dist['short']}) | 中等({dist['medium']}) | "
                        f"长({dist['long']}) | 很长({dist['very_long']})")
        
        # 时间分析
        if time_stats:
            report.append(f"\n⏰ 时间分析:")
            report.append(f"  • 覆盖天数: {time_stats['total_days_covered']}天")
            report.append(f"  • 最近24小时文章: {time_stats['recent_articles_24h']}篇")
            report.append(f"  • 高峰时段: {time_stats['peak_hour']}点 ({time_stats['peak_hour_count']}篇文章)")
        
        report.append("\n" + "=" * 50)
        
        return "\n".join(report)
    
    def save_statistics(self, output_path: str = None):
        """保存统计信息到文件"""
        if not output_path:
            output_path = os.path.join("output", "statistics.txt")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        report = self.generate_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"统计报告已保存到: {output_path}")
        
        return output_path
    
    def print_statistics(self):
        """打印统计信息到控制台"""
        print(self.generate_report())


def main():
    """测试函数"""
    stats_service = StatisticsService()
    stats_service.print_statistics()


if __name__ == "__main__":
    main() 