"""
기본 크롤러 클래스 - 공통 기능 통합
"""
import requests
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from config import SPRING_SERVER_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class BaseCrawler(ABC):
    """크롤러 기본 클래스"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def crawl(self) -> List[Dict]:
        """크롤링 실행 - 하위 클래스에서 구현"""
        pass
    
    def send_to_spring(self, data: Dict, endpoint: str, api_key: Optional[str] = None) -> bool:
        """스프링 서버로 데이터 전송"""
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["X-Crawler-API-Key"] = api_key
        
        try:
            response = requests.post(
                f"{SPRING_SERVER_URL}{endpoint}",
                json=data,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                logger.info(f"{self.source_name} 데이터 전송 성공")
                return True
            else:
                logger.error(f"{self.source_name} 전송 실패: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"{self.source_name} 전송 예외: {e}")
            return False
    
    def safe_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        """안전한 HTTP 요청"""
        try:
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"{self.source_name} 요청 실패 ({url}): {e}")
            return None