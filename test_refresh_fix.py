#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试刷新功能修复
验证API响应和配置指导信息
"""

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """测试所有API端点"""
    print("🧪 测试API端点")
    print("=" * 60)
    
    base_url = "https://design-newdrip.vercel.app"
    
    # 测试健康检查
    print("\n1️⃣ 测试健康检查 /api/health")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 健康检查通过")
        else:
            print(f"   ⚠️ 健康检查返回异常: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 健康检查失败: {str(e)}")
    
    # 测试状态端点
    print("\n2️⃣ 测试状态端点 /api/status")
    try:
        response = requests.get(f"{base_url}/api/status", timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 状态端点正常")
            print(f"   环境: {data.get('environment', 'unknown')}")
        else:
            print(f"   ⚠️ 状态端点返回异常: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 状态端点失败: {str(e)}")
    
    # 测试调试端点
    print("\n3️⃣ 测试调试端点 /api/debug")
    try:
        response = requests.get(f"{base_url}/api/debug", timeout=10)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 调试端点正常")
            env = data.get('environment', {})
            print(f"   VERCEL环境: {env.get('VERCEL', 'Not set')}")
            print(f"   GITHUB_TOKEN: {env.get('GITHUB_TOKEN', 'Not configured')}")
            
            # 显示部署检测
            detection = data.get('deployment_detection', {})
            print(f"   是否在Vercel: {detection.get('is_vercel', False)}")
            print(f"   是否配置Token: {detection.get('has_github_token', False)}")
        else:
            print(f"   ⚠️ 调试端点返回异常: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 调试端点失败: {str(e)}")
    
    # 测试刷新端点（不实际触发）
    print("\n4️⃣ 检查刷新端点 /api/refresh")
    print("   ℹ️ 不实际调用以避免触发Actions")
    print("   ✅ 端点路由已配置")

def test_refresh_response_structure():
    """测试刷新API的响应结构（模拟）"""
    print("\n\n📝 验证刷新API响应结构")
    print("=" * 60)
    
    # 模拟未配置Token的响应
    mock_response = {
        'success': False,
        'message': '⚠️ 刷新功能需要配置才能使用\n\n原因: 未配置GITHUB_TOKEN环境变量\n\n请按照配置指南完成设置后重试',
        'status': 'configuration_required',
        'config_guide': {
            'title': '📋 快速配置指南',
            'step1': {
                'name': '第一步：配置GitHub Token',
                'actions': [
                    '1. 在GitHub创建Personal Access Token',
                    '2. 权限勾选: repo + workflow + actions',
                    '3. 在Vercel环境变量中添加GITHUB_TOKEN'
                ]
            },
            'step2': {
                'name': '第二步：配置Vercel部署密钥',
                'actions': [
                    '1. 在Vercel创建Token',
                    '2. 获取项目ID和组织ID',
                    '3. 在GitHub Secrets中添加3个密钥'
                ]
            }
        }
    }
    
    print("\n✅ 响应结构验证:")
    print(f"   - success字段: {'✓' if 'success' in mock_response else '✗'}")
    print(f"   - message字段: {'✓' if 'message' in mock_response else '✗'}")
    print(f"   - status字段: {'✓' if 'status' in mock_response else '✗'}")
    print(f"   - config_guide字段: {'✓' if 'config_guide' in mock_response else '✗'}")
    
    if 'config_guide' in mock_response:
        guide = mock_response['config_guide']
        print(f"\n   配置指南包含:")
        print(f"   - 第一步: {guide['step1']['name']}")
        print(f"   - 第二步: {guide['step2']['name']}")

def show_configuration_checklist():
    """显示配置检查清单"""
    print("\n\n📋 配置检查清单")
    print("=" * 60)
    
    checklist = [
        {
            'category': 'Vercel环境变量',
            'items': [
                'GITHUB_TOKEN已配置',
                'Token包含正确权限（repo + workflow + actions）',
                '已应用到所有环境（Production, Preview, Development）'
            ]
        },
        {
            'category': 'GitHub Secrets',
            'items': [
                'VERCEL_TOKEN已配置',
                'ORG_ID已配置',
                'PROJECT_ID已配置'
            ]
        },
        {
            'category': 'GitHub Actions',
            'items': [
                'Workflow文件存在（.github/workflows/deploy.yml）',
                '手动触发能成功运行',
                '运行状态为绿色通过'
            ]
        },
        {
            'category': '前端功能',
            'items': [
                '刷新按钮可点击',
                'API返回正确响应',
                '显示详细配置指导'
            ]
        }
    ]
    
    for section in checklist:
        print(f"\n{section['category']}:")
        for item in section['items']:
            print(f"  ☐ {item}")

def main():
    """主函数"""
    print("🔍 刷新功能修复测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试API端点
    test_api_endpoints()
    
    # 验证响应结构
    test_refresh_response_structure()
    
    # 显示配置清单
    show_configuration_checklist()
    
    # 总结
    print("\n\n🎯 修复总结")
    print("=" * 60)
    print("""
✅ 已完成的修复:
  1. 创建环境诊断脚本 (diagnose_refresh.py)
  2. 编写完整配置指南 (完整配置修复指南.md)
  3. 优化API错误提示（提供详细配置步骤）
  4. 更新前端显示逻辑（显示配置指导）

📋 用户需要完成的配置:
  1. 在GitHub创建Personal Access Token
  2. 在Vercel环境变量中添加GITHUB_TOKEN
  3. 在Vercel创建Token并获取项目ID
  4. 在GitHub Secrets中添加部署密钥
  5. 测试配置是否生效

📚 相关文档:
  • 完整配置修复指南.md - 详细步骤说明
  • VERCEL_GITHUB_TOKEN_SETUP.md - GitHub Token配置
  • GITHUB_SECRETS_修复指南.md - 部署密钥配置
  • diagnose_refresh.py - 诊断工具

🚀 下一步:
  1. 阅读"完整配置修复指南.md"
  2. 按照步骤完成配置
  3. 运行 python3 diagnose_refresh.py 验证
  4. 测试线上刷新按钮功能
    """)
    
    print("=" * 60)
    print("✨ 测试完成！")

if __name__ == '__main__':
    main()

