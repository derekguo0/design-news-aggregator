#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刷新功能诊断工具
用于检测和诊断线上刷新功能的配置问题
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple

class RefreshDiagnostics:
    """刷新功能诊断类"""
    
    def __init__(self):
        self.issues: List[Dict] = []
        self.recommendations: List[str] = []
        
    def run_full_diagnosis(self) -> Dict:
        """运行完整诊断"""
        print("🔍 开始诊断刷新功能...")
        print("=" * 60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'environment': self.check_environment(),
            'api': self.check_api(),
            'github': self.check_github(),
            'issues': self.issues,
            'recommendations': self.recommendations,
            'overall_status': 'unknown'
        }
        
        # 判断整体状态
        if not self.issues:
            results['overall_status'] = 'healthy'
        elif len(self.issues) > 3:
            results['overall_status'] = 'critical'
        else:
            results['overall_status'] = 'warning'
            
        self.print_report(results)
        return results
    
    def check_environment(self) -> Dict:
        """检查环境配置"""
        print("\n📦 检查环境配置...")
        
        env_check = {
            'python_version': os.sys.version,
            'working_directory': os.getcwd(),
            'key_files': {}
        }
        
        # 检查关键文件
        key_files = [
            'api/refresh.py',
            'actions_refresh.py',
            '.github/workflows/deploy.yml',
            'config/sources.json',
            'templates/base.html',
            'vercel.json'
        ]
        
        for file_path in key_files:
            exists = os.path.exists(file_path)
            env_check['key_files'][file_path] = 'exists' if exists else 'missing'
            
            if not exists:
                self.issues.append({
                    'severity': 'high',
                    'component': 'files',
                    'message': f'关键文件缺失: {file_path}'
                })
        
        # 检查依赖
        try:
            import feedparser
            import jinja2
            import requests
            env_check['dependencies'] = 'installed'
            print("  ✅ Python依赖已安装")
        except ImportError as e:
            env_check['dependencies'] = f'missing: {str(e)}'
            self.issues.append({
                'severity': 'high',
                'component': 'dependencies',
                'message': f'缺少Python依赖: {str(e)}'
            })
            print(f"  ❌ 缺少依赖: {str(e)}")
        
        return env_check
    
    def check_api(self) -> Dict:
        """检查API端点"""
        print("\n🌐 检查API端点...")
        
        api_check = {
            'local': {},
            'production': {}
        }
        
        # 检查线上API（如果有URL）
        prod_url = os.environ.get('VERCEL_URL') or 'https://design-newdrip.vercel.app'
        
        endpoints = [
            '/api/health',
            '/api/status',
            '/api/debug'
        ]
        
        for endpoint in endpoints:
            url = f"{prod_url}{endpoint}"
            try:
                response = requests.get(url, timeout=10)
                api_check['production'][endpoint] = {
                    'status': response.status_code,
                    'accessible': response.status_code == 200
                }
                
                if response.status_code == 200:
                    print(f"  ✅ {endpoint}: 可访问")
                else:
                    print(f"  ⚠️ {endpoint}: HTTP {response.status_code}")
                    self.issues.append({
                        'severity': 'medium',
                        'component': 'api',
                        'message': f'API端点返回异常状态: {endpoint} ({response.status_code})'
                    })
            except requests.exceptions.RequestException as e:
                api_check['production'][endpoint] = {
                    'accessible': False,
                    'error': str(e)
                }
                print(f"  ❌ {endpoint}: 无法访问 ({str(e)})")
                self.issues.append({
                    'severity': 'high',
                    'component': 'api',
                    'message': f'无法访问API端点: {endpoint}'
                })
        
        return api_check
    
    def check_github(self) -> Dict:
        """检查GitHub配置"""
        print("\n🔧 检查GitHub配置...")
        
        github_check = {
            'workflow_file': False,
            'repository_accessible': False,
            'recent_runs': []
        }
        
        # 检查workflow文件
        workflow_path = '.github/workflows/deploy.yml'
        if os.path.exists(workflow_path):
            github_check['workflow_file'] = True
            print(f"  ✅ Workflow文件存在")
        else:
            github_check['workflow_file'] = False
            print(f"  ❌ Workflow文件缺失")
            self.issues.append({
                'severity': 'critical',
                'component': 'github',
                'message': 'GitHub Actions workflow配置文件缺失'
            })
        
        # 检查GitHub仓库可访问性
        repo = os.environ.get('GITHUB_REPOSITORY', 'derekguo0/design-news-aggregator')
        repo_url = f"https://api.github.com/repos/{repo}"
        
        try:
            response = requests.get(repo_url, timeout=10)
            if response.status_code == 200:
                github_check['repository_accessible'] = True
                print(f"  ✅ GitHub仓库可访问")
            else:
                print(f"  ⚠️ 仓库访问返回: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ❌ 无法访问GitHub仓库: {str(e)}")
        
        # 检查最近的Actions运行
        actions_url = f"https://api.github.com/repos/{repo}/actions/runs?per_page=5"
        try:
            response = requests.get(actions_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                runs = data.get('workflow_runs', [])
                
                if runs:
                    print(f"  📊 最近的Actions运行:")
                    for run in runs[:3]:
                        status = run.get('conclusion', run.get('status'))
                        created_at = run.get('created_at', '')
                        print(f"     • {status}: {created_at}")
                        
                        if status == 'failure':
                            self.issues.append({
                                'severity': 'high',
                                'component': 'github_actions',
                                'message': f'GitHub Actions运行失败: {created_at}'
                            })
                    
                    github_check['recent_runs'] = [
                        {
                            'status': r.get('conclusion', r.get('status')),
                            'created_at': r.get('created_at')
                        } for r in runs[:5]
                    ]
                else:
                    print(f"  ℹ️ 没有Actions运行记录")
        except Exception as e:
            print(f"  ⚠️ 无法获取Actions历史: {str(e)}")
        
        return github_check
    
    def print_report(self, results: Dict):
        """打印诊断报告"""
        print("\n" + "=" * 60)
        print("📋 诊断报告")
        print("=" * 60)
        
        status = results['overall_status']
        status_emoji = {
            'healthy': '✅',
            'warning': '⚠️',
            'critical': '❌',
            'unknown': '❓'
        }
        
        print(f"\n总体状态: {status_emoji.get(status, '❓')} {status.upper()}")
        print(f"诊断时间: {results['timestamp']}")
        
        if self.issues:
            print(f"\n🚨 发现 {len(self.issues)} 个问题:")
            for i, issue in enumerate(self.issues, 1):
                severity_emoji = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🟢'
                }
                emoji = severity_emoji.get(issue['severity'], '⚪')
                print(f"  {i}. {emoji} [{issue['component']}] {issue['message']}")
        else:
            print("\n✅ 未发现配置问题")
        
        # 生成建议
        self.generate_recommendations()
        
        if self.recommendations:
            print(f"\n💡 修复建议:")
            for i, rec in enumerate(self.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "=" * 60)
    
    def generate_recommendations(self):
        """生成修复建议"""
        if not self.issues:
            return
        
        # 根据问题类型生成建议
        has_api_issues = any(i['component'] == 'api' for i in self.issues)
        has_github_issues = any(i['component'] in ['github', 'github_actions'] for i in self.issues)
        has_file_issues = any(i['component'] == 'files' for i in self.issues)
        
        if has_api_issues:
            self.recommendations.append(
                "检查Vercel部署状态，确认API端点已正确部署"
            )
            self.recommendations.append(
                "验证vercel.json中的路由配置是否正确"
            )
        
        if has_github_issues:
            self.recommendations.append(
                "配置GitHub Token: 在Vercel环境变量中添加GITHUB_TOKEN"
            )
            self.recommendations.append(
                "配置Vercel部署密钥: 在GitHub Secrets中添加VERCEL_TOKEN, ORG_ID, PROJECT_ID"
            )
            self.recommendations.append(
                "查看详细配置指南: VERCEL_GITHUB_TOKEN_SETUP.md 和 GITHUB_SECRETS_修复指南.md"
            )
        
        if has_file_issues:
            self.recommendations.append(
                "恢复缺失的关键文件，或从Git仓库重新拉取代码"
            )
        
        # 通用建议
        self.recommendations.append(
            "运行测试脚本验证修复: python3 test_api_simple.py"
        )
        self.recommendations.append(
            "查看完整文档: 使用指南.md"
        )

def main():
    """主函数"""
    print("🔍 设计资讯刷新功能诊断工具")
    print("=" * 60)
    
    diagnostics = RefreshDiagnostics()
    results = diagnostics.run_full_diagnosis()
    
    # 保存诊断结果
    output_file = f"diagnosis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 诊断报告已保存到: {output_file}")
    except Exception as e:
        print(f"\n⚠️ 无法保存报告: {str(e)}")
    
    print("\n📚 相关文档:")
    print("  • VERCEL_GITHUB_TOKEN_SETUP.md - GitHub Token配置指南")
    print("  • GITHUB_SECRETS_修复指南.md - Vercel部署密钥配置")
    print("  • 线上刷新功能说明.md - 刷新功能工作原理")
    print("  • 使用指南.md - 完整使用文档")

if __name__ == '__main__':
    main()

