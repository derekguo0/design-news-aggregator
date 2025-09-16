#!/usr/bin/env python3
"""
测试刷新API是否正常工作
"""

import requests
import json

def test_refresh_api():
    """测试刷新API"""
    try:
        print("🔍 测试刷新API...")
        
        # 测试本地API（如果有的话）
        local_url = "http://localhost:3000/api/refresh"
        
        # 测试线上API
        online_url = "https://design-news-aggregator.vercel.app/api/refresh"
        
        for name, url in [("线上", online_url)]:
            print(f"\n📡 测试 {name} API: {url}")
            
            try:
                response = requests.post(url, 
                                       headers={'Content-Type': 'application/json'},
                                       timeout=30)
                
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print("✅ API响应成功")
                    print(f"Success: {data.get('success')}")
                    print(f"Message: {data.get('message')}")
                    print(f"Deployment Type: {data.get('deployment_type')}")
                    
                    if 'result' in data:
                        result = data['result']
                        print(f"Result keys: {list(result.keys())}")
                        if 'items' in result:
                            items = result['items']
                            print(f"Items count: {len(items)}")
                            if items:
                                print(f"First item: {items[0]}")
                        else:
                            print("⚠️ Result中没有items字段")
                    else:
                        print("⚠️ 响应中没有result字段")
                        
                    print(f"完整响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                else:
                    print(f"❌ API响应错误: {response.status_code}")
                    print(f"响应内容: {response.text}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ {name} API 超时")
            except requests.exceptions.ConnectionError:
                print(f"🔌 {name} API 连接失败")
            except Exception as e:
                print(f"❌ {name} API 测试失败: {e}")

if __name__ == "__main__":
    test_refresh_api()
