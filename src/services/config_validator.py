#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
配置验证模块
验证配置文件的完整性和有效性
"""

import os
import requests
import feedparser
from typing import Dict, List, Tuple, Any
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """验证所有配置
        
        Returns:
            Tuple[bool, List[str], List[str]]: (是否通过验证, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []
        
        # 验证基础环境
        self._validate_environment()
        
        # 验证目录结构
        self._validate_directories()
        
        # 验证API密钥
        self._validate_api_keys()
        
        # 验证RSS源
        self._validate_rss_sources()
        
        # 验证模板文件
        self._validate_templates()
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_environment(self):
        """验证运行环境"""
        try:
            # 检查Python版本
            import sys
            if sys.version_info < (3, 7):
                self.errors.append("需要Python 3.7或更高版本")
            
            # 检查必要的包
            required_packages = [
                'feedparser', 'requests', 'jinja2', 'loguru'
            ]
            
            missing_packages = []
            for package in required_packages:
                try:
                    __import__(package)
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                self.errors.append(f"缺少必要的包: {', '.join(missing_packages)}")
                self.errors.append("请运行: pip install -r requirements.txt")
                
        except Exception as e:
            self.errors.append(f"环境检查失败: {e}")
    
    def _validate_directories(self):
        """验证目录结构"""
        required_dirs = [
            'src',
            'templates',
            'output',
            'data',
            'logs'
        ]
        
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                if dir_name in ['output', 'data', 'logs']:
                    # 这些目录可以自动创建
                    try:
                        os.makedirs(dir_name, exist_ok=True)
                        self.warnings.append(f"已自动创建目录: {dir_name}")
                    except Exception as e:
                        self.errors.append(f"无法创建目录 {dir_name}: {e}")
                else:
                    self.errors.append(f"缺少必要目录: {dir_name}")
    
    def _validate_api_keys(self):
        """验证API密钥"""
        try:
            from ..config import Config
            config = Config()
            
            # 检查OpenAI API密钥
            openai_key = getattr(config, 'OPENAI_API_KEY', None)
            if not openai_key or openai_key == "your-openai-api-key-here":
                self.warnings.append("OpenAI API密钥未配置，AI分析功能将被禁用")
            else:
                # 验证API密钥格式
                if not openai_key.startswith('sk-'):
                    self.warnings.append("OpenAI API密钥格式可能不正确")
                    
                # 可以添加API密钥有效性测试（需要谨慎，避免频繁调用）
                # self._test_openai_api(openai_key)
            
            # 检查其他API密钥
            anthropic_key = getattr(config, 'ANTHROPIC_API_KEY', None)
            if anthropic_key and anthropic_key != "your-anthropic-api-key-here":
                self.warnings.append("检测到Anthropic API密钥配置")
            
        except Exception as e:
            self.warnings.append(f"API密钥验证失败: {e}")
    
    def _validate_rss_sources(self):
        """验证RSS源配置"""
        try:
            from ..config import Config
            config = Config()
            
            if not hasattr(config, 'RSS_SOURCES') or not config.RSS_SOURCES:
                self.errors.append("RSS源配置为空")
                return
            
            valid_sources = 0
            total_sources = len(config.RSS_SOURCES)
            
            for i, source in enumerate(config.RSS_SOURCES):
                source_name = source.get('name', f'源{i+1}')
                source_url = source.get('url', '')
                
                if not source_url:
                    self.errors.append(f"RSS源 '{source_name}' 缺少URL")
                    continue
                
                # 验证URL格式
                try:
                    parsed = urlparse(source_url)
                    if not all([parsed.scheme, parsed.netloc]):
                        self.errors.append(f"RSS源 '{source_name}' URL格式无效: {source_url}")
                        continue
                except Exception:
                    self.errors.append(f"RSS源 '{source_name}' URL解析失败: {source_url}")
                    continue
                
                # 测试RSS源可访问性（可选，避免启动时过慢）
                if hasattr(config, 'VALIDATE_RSS_ON_STARTUP') and config.VALIDATE_RSS_ON_STARTUP:
                    if self._test_rss_source(source_url, source_name):
                        valid_sources += 1
                else:
                    valid_sources += 1
            
            if valid_sources == 0:
                self.errors.append("没有有效的RSS源")
            elif valid_sources < total_sources:
                self.warnings.append(f"有 {total_sources - valid_sources} 个RSS源可能无法访问")
                
        except Exception as e:
            self.errors.append(f"RSS源验证失败: {e}")
    
    def _test_rss_source(self, url: str, name: str) -> bool:
        """测试RSS源可访问性"""
        try:
            # 使用feedparser测试
            feed = feedparser.parse(url)
            
            if feed.bozo and feed.bozo_exception:
                self.warnings.append(f"RSS源 '{name}' 可能有问题: {feed.bozo_exception}")
                return False
            
            if not feed.entries:
                self.warnings.append(f"RSS源 '{name}' 没有条目")
                return False
            
            return True
            
        except Exception as e:
            self.warnings.append(f"RSS源 '{name}' 测试失败: {e}")
            return False
    
    def _validate_templates(self):
        """验证模板文件"""
        required_templates = [
            'templates/index.html',
            'templates/daily.html'
        ]
        
        for template_path in required_templates:
            if not os.path.exists(template_path):
                self.errors.append(f"缺少模板文件: {template_path}")
            else:
                # 验证模板语法
                try:
                    from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError
                    env = Environment(loader=FileSystemLoader('templates'))
                    template_name = os.path.basename(template_path)
                    env.get_template(template_name)
                except TemplateSyntaxError as e:
                    self.errors.append(f"模板 {template_path} 语法错误: {e}")
                except Exception as e:
                    self.warnings.append(f"模板 {template_path} 验证失败: {e}")
    
    def _test_openai_api(self, api_key: str):
        """测试OpenAI API密钥有效性（谨慎使用）"""
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # 使用最简单的API调用进行测试
            response = requests.get(
                'https://api.openai.com/v1/models',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 401:
                self.errors.append("OpenAI API密钥无效")
            elif response.status_code == 429:
                self.warnings.append("OpenAI API调用频率限制")
            elif response.status_code != 200:
                self.warnings.append(f"OpenAI API响应异常: {response.status_code}")
                
        except requests.RequestException:
            self.warnings.append("无法连接到OpenAI API（可能是网络问题）")
        except Exception as e:
            self.warnings.append(f"OpenAI API测试失败: {e}")
    
    def generate_report(self) -> str:
        """生成验证报告"""
        report = []
        report.append("🔍 配置验证报告")
        report.append("=" * 40)
        
        if not self.errors and not self.warnings:
            report.append("\n✅ 所有配置检查通过！")
        else:
            if self.errors:
                report.append(f"\n❌ 发现 {len(self.errors)} 个错误:")
                for i, error in enumerate(self.errors, 1):
                    report.append(f"  {i}. {error}")
            
            if self.warnings:
                report.append(f"\n⚠️  发现 {len(self.warnings)} 个警告:")
                for i, warning in enumerate(self.warnings, 1):
                    report.append(f"  {i}. {warning}")
        
        report.append("\n" + "=" * 40)
        return "\n".join(report)
    
    def print_report(self):
        """打印验证报告"""
        print(self.generate_report())


def validate_config() -> bool:
    """验证配置的便捷函数"""
    validator = ConfigValidator()
    is_valid, errors, warnings = validator.validate_all()
    validator.print_report()
    return is_valid


def main():
    """测试函数"""
    validate_config()


if __name__ == "__main__":
    main() 