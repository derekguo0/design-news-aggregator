#!/usr/bin/env python3
"""
调试用的GitHub Actions脚本
简化版本，专门用来排查CI/CD问题
"""

import sys
import os
from datetime import datetime
from pathlib import Path

def debug_environment():
    """调试环境信息"""
    print("🔍 GitHub Actions 环境调试")
    print("=" * 50)
    
    print(f"🐍 Python版本: {sys.version}")
    print(f"📁 工作目录: {Path.cwd()}")
    print(f"🌍 环境变量:")
    
    # 检查重要的环境变量
    important_vars = ['GITHUB_TOKEN', 'GITHUB_REPOSITORY', 'GITHUB_WORKSPACE', 'RUNNER_OS']
    for var in important_vars:
        value = os.environ.get(var, '未设置')
        if var == 'GITHUB_TOKEN' and value != '未设置':
            value = f"{value[:8]}..." if len(value) > 8 else value
        print(f"   {var}: {value}")
    
    print(f"\n📂 目录结构:")
    for item in sorted(Path.cwd().iterdir()):
        if item.is_dir():
            print(f"   📁 {item.name}/")
        else:
            print(f"   📄 {item.name}")
    
    # 检查关键目录
    print(f"\n🔍 关键目录检查:")
    key_dirs = ['src', 'data', 'output', 'config']
    for dir_name in key_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   ✅ {dir_name}/ 存在")
        else:
            print(f"   ❌ {dir_name}/ 不存在")
    
    # 检查关键文件
    print(f"\n📄 关键文件检查:")
    key_files = ['requirements.txt', 'config/sources.json', 'actions_refresh.py']
    for file_name in key_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"   ✅ {file_name} 存在")
        else:
            print(f"   ❌ {file_name} 不存在")

def simple_content_generation():
    """简化的内容生成测试"""
    print(f"\n🚀 简化内容生成测试")
    print("-" * 30)
    
    try:
        # 添加src到路径
        sys.path.insert(0, str(Path.cwd() / "src"))
        print("✅ 已添加src目录到Python路径")
        
        # 尝试导入
        try:
            from src.config import get_config
            print("✅ 成功导入配置模块")
        except ImportError as e:
            print(f"❌ 导入配置模块失败: {e}")
            return False
        
        try:
            from src.scheduler.task_scheduler import TaskScheduler
            print("✅ 成功导入调度器模块")
        except ImportError as e:
            print(f"❌ 导入调度器模块失败: {e}")
            return False
        
        # 创建必要的目录
        output_dir = Path("output")
        data_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        data_dir.mkdir(exist_ok=True)
        print(f"✅ 创建目录: {output_dir}, {data_dir}")
        
        # 创建简单的测试文件
        today = datetime.now().strftime('%Y-%m-%d')
        test_data = {
            "date": f"{today}T00:00:00",
            "total_items": 1,
            "items": [{
                "title": "测试资讯",
                "url": "https://example.com",
                "source": "测试源",
                "category": "测试",
                "summary": "这是一个测试资讯",
                "published_at": f"{today}T00:00:00"
            }],
            "sources": ["测试源"],
            "generated_at": f"{today}T{datetime.now().strftime('%H:%M:%S')}"
        }
        
        # 保存测试数据
        import json
        with open(data_dir / f"digest-{today}.json", 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 创建测试数据文件: digest-{today}.json")
        
        # 创建简单的HTML文件
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试页面 - {today}</title>
</head>
<body>
    <h1>GitHub Actions 测试成功</h1>
    <p>生成时间: {datetime.now()}</p>
    <p>这是一个由GitHub Actions生成的测试页面</p>
</body>
</html>"""
        
        with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 创建测试HTML文件: index.html")
        
        with open(output_dir / f"daily-{today}.html", 'w', encoding='utf-8') as f:
            f.write(html_content.replace("测试页面", f"每日页面 {today}"))
        print(f"✅ 创建每日HTML文件: daily-{today}.html")
        
        return True
        
    except Exception as e:
        print(f"❌ 简化生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print(f"🤖 GitHub Actions 调试脚本")
    print(f"🕒 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # 环境调试
    debug_environment()
    
    # 简化内容生成
    success = simple_content_generation()
    
    if success:
        print(f"\n🎉 调试脚本执行成功!")
        print(f"📦 测试文件已生成")
        sys.exit(0)
    else:
        print(f"\n💥 调试脚本执行失败!")
        sys.exit(1)

if __name__ == "__main__":
    main()
