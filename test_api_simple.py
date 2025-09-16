#!/usr/bin/env python3
import requests
import json

def test_api():
    url = "https://design-news-aggregator.vercel.app/api/refresh"
    print(f"测试API: {url}")
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("API响应成功")
            print(f"Success: {data.get('success')}")
            print(f"Message: {data.get('message')}")
            
            if 'result' in data:
                result = data['result']
                print(f"Result keys: {list(result.keys())}")
                if 'items' in result:
                    items = result['items']
                    print(f"Items count: {len(items)}")
                    if items:
                        print(f"First item keys: {list(items[0].keys())}")
                        print(f"First item title: {items[0].get('title')}")
        else:
            print(f"API错误: {response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_api()
