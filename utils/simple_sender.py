"""
간단한 데이터 전송 유틸리티
"""
import requests
import logging
from typing import Dict
from config import SPRING_SERVER_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

def send_to_spring(data: Dict, endpoint: str, source_name: str) -> bool:
    """스프링 서버로 데이터 전송 (Public API)"""
    try:
        response = requests.post(
            f"{SPRING_SERVER_URL}{endpoint}",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"✅ {source_name} 전송 성공: {data.get('title', '')[:30]}...")
            return True
        else:
            logger.error(f"❌ {source_name} 전송 실패: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ {source_name} 전송 예외: {e}")
        return False

def send_to_spring_admin(data: Dict, endpoint: str, source_name: str, api_key: str = None) -> bool:
    """스프링 서버로 데이터 전송 (Admin API)"""
    from config import API_KEY
    
    # API 키가 지정되지 않으면 기본 키 사용
    if api_key is None:
        api_key = API_KEY
    
    try:
        response = requests.post(
            f"{SPRING_SERVER_URL}{endpoint}",
            json=data,
            headers={
                "Content-Type": "application/json",
                "X-Crawler-API-Key": api_key
            },
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"✅ {source_name} Admin 전송 성공: {data.get('title', '')[:30]}...")
            return True
        else:
            logger.error(f"❌ {source_name} Admin 전송 실패: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ {source_name} Admin 전송 예외: {e}")
        return False