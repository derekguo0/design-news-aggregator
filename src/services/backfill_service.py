"""
历史内容补全服务
检查和补全缺失的历史日期内容
"""

import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Any, Tuple
from loguru import logger

from ..models import DailyDigest, NewsItem, CategorySummary


class BackfillService:
    """历史内容补全服务"""
    
    def __init__(self, data_dir: str = "data", output_dir: str = "output"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        
        # 确保目录存在
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def find_missing_dates(self, start_date: date = None, end_date: date = None) -> List[str]:
        """查找缺失的日期"""
        try:
            # 获取现有的数据文件
            existing_files = list(self.data_dir.glob("digest-*.json"))
            existing_dates = []
            
            for file in existing_files:
                try:
                    date_str = file.stem.replace("digest-", "")
                    datetime.strptime(date_str, "%Y-%m-%d")  # 验证日期格式
                    existing_dates.append(date_str)
                except ValueError:
                    continue
            
            if not existing_dates:
                logger.warning("没有找到任何现有的数据文件")
                return []
            
            existing_dates.sort()
            
            # 确定日期范围
            if start_date is None:
                start_date = datetime.strptime(existing_dates[0], "%Y-%m-%d").date()
            if end_date is None:
                end_date = datetime.strptime(existing_dates[-1], "%Y-%m-%d").date()
            
            # 查找缺失的日期
            missing_dates = []
            current_date = start_date
            
            while current_date <= end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                if date_str not in existing_dates:
                    missing_dates.append(date_str)
                current_date += timedelta(days=1)
            
            logger.info(f"发现 {len(missing_dates)} 个缺失日期: {missing_dates}")
            return missing_dates
            
        except Exception as e:
            logger.error(f"查找缺失日期失败: {e}")
            return []
    
    def create_placeholder_digest(self, target_date: str) -> DailyDigest:
        """为指定日期创建占位摘要"""
        try:
            date_obj = datetime.strptime(target_date, "%Y-%m-%d")
            
            # 创建空的分类摘要
            placeholder_digest = DailyDigest(
                date=date_obj,
                categories=[],
                total_items=0,
                sources=[]
            )
            
            logger.info(f"为日期 {target_date} 创建占位摘要")
            return placeholder_digest
            
        except Exception as e:
            logger.error(f"创建占位摘要失败: {e}")
            raise
    
    def create_placeholder_data(self, target_date: str) -> Dict[str, Any]:
        """创建占位数据文件内容"""
        return {
            "date": f"{target_date}T00:00:00",
            "total_items": 0,
            "categories": [],
            "sources": [],
            "generated_at": datetime.now().isoformat(),
            "metadata": {
                "note": f"此日期暂无资讯内容 ({target_date})",
                "status": "placeholder",
                "reason": "历史数据自动补全",
                "backfilled_at": datetime.now().isoformat()
            }
        }
    
    def create_placeholder_html(self, target_date: str) -> str:
        """创建占位HTML页面"""
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
    <style>
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto py-8 px-4">
        <header class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">{chinese_date}</h1>
            <p class="text-lg text-gray-600">{chinese_weekday}</p>
            <div class="mt-4 text-sm text-gray-500">
                <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">自动补全</span>
            </div>
        </header>
        
        <div class="bg-white rounded-xl shadow-sm border p-8 text-center">
            <div class="text-6xl mb-4">📰</div>
            <h2 class="text-xl font-semibold text-gray-700 mb-2">暂无资讯内容</h2>
            <p class="text-gray-500 mb-6">此日期的资讯内容已通过自动补全功能添加，但暂无实际内容。</p>
            
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <div class="text-blue-600 text-sm">
                    <p class="font-medium mb-1">💡 提示</p>
                    <p>这是系统自动生成的占位页面，用于保持归档的连续性。</p>
                </div>
            </div>
            
            <div class="flex justify-center space-x-4">
                <a href="/" class="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                    🏠 返回首页
                </a>
                <a href="/archive.html" class="inline-flex items-center px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors">
                    📁 查看归档
                </a>
            </div>
        </div>
        
        <div class="mt-8 text-center text-sm text-gray-400">
            <p>由刷新功能自动补全 • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>'''
        
        return html_content
    
    def backfill_missing_dates(self, missing_dates: List[str]) -> Tuple[int, int]:
        """补全缺失的日期内容"""
        created_data_files = 0
        created_html_files = 0
        
        try:
            for date_str in missing_dates:
                logger.info(f"补全日期: {date_str}")
                
                # 创建数据文件
                json_filename = f"digest-{date_str}.json"
                json_path = self.data_dir / json_filename
                
                if not json_path.exists():
                    placeholder_data = self.create_placeholder_data(date_str)
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(placeholder_data, f, ensure_ascii=False, indent=2)
                    logger.success(f"创建数据文件: {json_filename}")
                    created_data_files += 1
                
                # 创建HTML页面
                html_filename = f"daily-{date_str}.html"
                html_path = self.output_dir / html_filename
                
                if not html_path.exists():
                    placeholder_html = self.create_placeholder_html(date_str)
                    with open(html_path, 'w', encoding='utf-8') as f:
                        f.write(placeholder_html)
                    logger.success(f"创建页面文件: {html_filename}")
                    created_html_files += 1
            
            logger.success(f"补全完成: 创建了 {created_data_files} 个数据文件, {created_html_files} 个页面文件")
            return created_data_files, created_html_files
            
        except Exception as e:
            logger.error(f"补全缺失日期失败: {e}")
            raise
    
    def auto_backfill(self, max_days_back: int = 30) -> Dict[str, Any]:
        """自动补全功能：在刷新时调用"""
        try:
            logger.info("🔍 开始检查历史内容缺失...")
            
            # 计算检查范围：最近30天
            end_date = date.today()
            start_date = end_date - timedelta(days=max_days_back)
            
            # 查找缺失日期
            missing_dates = self.find_missing_dates(start_date, end_date)
            
            if not missing_dates:
                logger.info("✅ 没有发现缺失的历史内容")
                return {
                    'success': True,
                    'action': 'none',
                    'message': '历史内容完整，无需补全',
                    'missing_count': 0,
                    'created_files': 0
                }
            
            logger.info(f"📋 发现 {len(missing_dates)} 个缺失日期，开始补全...")
            
            # 补全缺失内容
            data_files, html_files = self.backfill_missing_dates(missing_dates)
            total_files = data_files + html_files
            
            result = {
                'success': True,
                'action': 'backfilled',
                'message': f'成功补全 {len(missing_dates)} 个缺失日期',
                'missing_count': len(missing_dates),
                'missing_dates': missing_dates,
                'created_files': total_files,
                'data_files': data_files,
                'html_files': html_files,
                'date_range': f"{start_date} 至 {end_date}"
            }
            
            logger.success(f"🎉 历史内容补全完成: {result['message']}")
            return result
            
        except Exception as e:
            logger.error(f"自动补全失败: {e}")
            return {
                'success': False,
                'action': 'failed',
                'message': f'补全失败: {str(e)}',
                'error': str(e)
            }