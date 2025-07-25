"""
飞书API客户端
实现文档创建和内容推送功能
"""
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
from loguru import logger

from ..config import get_config
from ..models import DailyDigest

class FeishuClient:
    """飞书API客户端"""
    
    def __init__(self):
        self.config = get_config().feishu
        self.base_url = "https://open.feishu.cn/open-apis"
        self.access_token = None
        self.token_expires_at = None
    
    def _get_access_token(self) -> str:
        """获取访问令牌"""
        # 检查token是否过期
        if (self.access_token and self.token_expires_at and 
            time.time() < self.token_expires_at - 300):  # 提前5分钟刷新
            return self.access_token
        
        # 获取新的access_token
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        
        payload = {
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret
        }
        
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if data.get("code") == 0:
                self.access_token = data["tenant_access_token"]
                # 设置过期时间 (通常2小时，这里设置为1.8小时)
                self.token_expires_at = time.time() + data.get("expire", 6300)
                logger.info("飞书访问令牌获取成功")
                return self.access_token
            else:
                raise Exception(f"获取访问令牌失败: {data}")
                
        except Exception as e:
            logger.error(f"获取飞书访问令牌失败: {e}")
            raise
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发起API请求"""
        url = f"{self.base_url}{endpoint}"
        
        headers = kwargs.get("headers", {})
        headers.update({
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json; charset=utf-8"
        })
        kwargs["headers"] = headers
        
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            
            data = response.json()
            if data.get("code") == 0:
                return data
            else:
                raise Exception(f"API请求失败: {data}")
                
        except Exception as e:
            logger.error(f"飞书API请求失败 {method} {endpoint}: {e}")
            raise
    
    def create_document(self, title: str, folder_token: str = None) -> str:
        """创建新文档"""
        endpoint = "/docx/v1/documents"
        
        payload = {
            "title": title,
            "type": "docx"
        }
        
        # 如果指定了文件夹，则在指定文件夹中创建
        if folder_token or self.config.folder_token:
            payload["folder_token"] = folder_token or self.config.folder_token
        
        try:
            response = self._make_request("POST", endpoint, json=payload)
            document_id = response["data"]["document"]["document_id"]
            
            logger.success(f"飞书文档创建成功: {title} (ID: {document_id})")
            return document_id
            
        except Exception as e:
            logger.error(f"创建飞书文档失败: {e}")
            raise
    
    def update_document_content(self, document_id: str, blocks: List[Dict[str, Any]]) -> bool:
        """更新文档内容"""
        endpoint = f"/docx/v1/documents/{document_id}/blocks/batch_update"
        
        # 批量更新请求
        payload = {
            "requests": []
        }
        
        # 为每个块创建插入请求
        for block in blocks:
            request = {
                "request_type": "INSERT_BLOCK_AFTER",
                "insert_block_after": {
                    "block_id": "doxcnDhK_b9tCi_LkMSKJLOc4Ah",  # 插入到文档末尾
                    "blocks": [block]
                }
            }
            payload["requests"].append(request)
        
        try:
            response = self._make_request("PATCH", endpoint, json=payload)
            logger.success(f"文档内容更新成功: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"更新文档内容失败: {e}")
            return False
    
    def add_blocks_to_document(self, document_id: str, blocks: List[Dict[str, Any]]) -> bool:
        """向文档添加内容块"""
        endpoint = f"/docx/v1/documents/{document_id}/blocks/batch_create"
        
        payload = {
            "blocks": blocks
        }
        
        try:
            response = self._make_request("POST", endpoint, json=payload)
            logger.success(f"向文档添加内容成功: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"向文档添加内容失败: {e}")
            return False
    
    def create_daily_report_document(self, digest: DailyDigest) -> Optional[str]:
        """创建每日报告文档"""
        try:
            # 生成文档标题
            title = f"{self.config.doc_title_prefix} - {digest.date.strftime('%Y年%m月%d日')}"
            
            # 创建文档
            document_id = self.create_document(title)
            
            # 获取飞书格式的内容块
            blocks = digest.to_feishu_blocks()
            
            # 添加内容到文档
            if self.add_blocks_to_document(document_id, blocks):
                logger.success(f"每日报告文档创建成功: {title}")
                return document_id
            else:
                logger.error("添加内容到文档失败")
                return None
                
        except Exception as e:
            logger.error(f"创建每日报告文档失败: {e}")
            return None
    
    def share_document(self, document_id: str, link_share_entity: str = "tenant") -> Optional[str]:
        """分享文档并获取分享链接"""
        endpoint = f"/drive/v1/permissions/{document_id}/public"
        
        payload = {
            "link_share_entity": link_share_entity,  # "anyone"或"tenant"
            "link_share_enable": True
        }
        
        try:
            response = self._make_request("PATCH", endpoint, json=payload)
            
            # 获取分享链接
            get_endpoint = f"/drive/v1/files/{document_id}"
            response = self._make_request("GET", get_endpoint)
            
            share_url = response["data"]["url"]
            logger.success(f"文档分享成功: {share_url}")
            return share_url
            
        except Exception as e:
            logger.error(f"分享文档失败: {e}")
            return None
    
    def send_notification(self, user_ids: List[str], title: str, content: str) -> bool:
        """发送通知消息"""
        endpoint = "/im/v1/messages"
        
        # 构建消息卡片
        card_content = {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": f"**{title}**\n\n{content}",
                        "tag": "lark_md"
                    }
                }
            ]
        }
        
        for user_id in user_ids:
            payload = {
                "receive_id": user_id,
                "msg_type": "interactive",
                "content": json.dumps(card_content)
            }
            
            try:
                response = self._make_request("POST", endpoint, json=payload)
                logger.info(f"通知发送成功: {user_id}")
                
            except Exception as e:
                logger.error(f"发送通知失败 {user_id}: {e}")
                return False
        
        return True
    
    def get_folder_contents(self, folder_token: str) -> List[Dict[str, Any]]:
        """获取文件夹内容"""
        endpoint = f"/drive/v1/files"
        
        params = {
            "parent_token": folder_token,
            "page_size": 100
        }
        
        try:
            response = self._make_request("GET", endpoint, params=params)
            return response["data"]["files"]
            
        except Exception as e:
            logger.error(f"获取文件夹内容失败: {e}")
            return []
    
    def test_connection(self) -> bool:
        """测试连接"""
        try:
            token = self._get_access_token()
            if token:
                logger.success("飞书API连接测试成功")
                return True
            else:
                logger.error("飞书API连接测试失败")
                return False
                
        except Exception as e:
            logger.error(f"飞书API连接测试失败: {e}")
            return False 