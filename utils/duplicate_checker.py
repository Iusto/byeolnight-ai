"""
중복 체크 및 재시도 로직
"""
import hashlib
import logging
from typing import Dict, List, Optional
import requests
from config import SPRING_SERVER_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

class DuplicateChecker:
    """중복 체크 및 재시도 처리 클래스"""
    
    def __init__(self):
        self.retry_count = 5  # 최대 재시도 횟수
        self.processed_hashes = set()  # 처리된 콘텐츠 해시 저장
    
    def generate_content_hash(self, title: str, content: str) -> str:
        """제목과 내용으로 해시 생성"""
        combined = f"{title.strip()}{content.strip()}"
        return hashlib.md5(combined.encode('utf-8')).hexdigest()
    
    def is_duplicate_content(self, title: str, content: str) -> bool:
        """로컬 중복 체크"""
        content_hash = self.generate_content_hash(title, content)
        if content_hash in self.processed_hashes:
            return True
        self.processed_hashes.add(content_hash)
        return False
    
    def check_server_duplicate(self, title: str, content: str) -> bool:
        """서버에서 중복 체크"""
        try:
            # 서버의 중복 체크 API 호출 (실제 구현에 맞게 수정)
            response = requests.post(
                f"{SPRING_SERVER_URL}/api/admin/crawler/check-duplicate",
                json={"title": title, "content": content[:100]},  # 내용 일부만 전송
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("isDuplicate", False)
            else:
                logger.warning(f"서버 중복 체크 실패: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"서버 중복 체크 예외: {e}")
            return False
    
    def send_with_retry(self, data: Dict, endpoint: str, source_name: str) -> bool:
        """중복 체크 및 재시도 로직으로 데이터 전송"""
        title = data.get("title", "")
        content = data.get("content", "")
        
        # 로컬 중복 체크
        if self.is_duplicate_content(title, content):
            logger.info(f"로컬 중복 감지 - 건너뜀: {title[:30]}...")
            return False
        
        # 서버 중복 체크 및 재시도
        for attempt in range(1, self.retry_count + 1):
            try:
                # 서버 중복 체크
                if self.check_server_duplicate(title, content):
                    logger.info(f"서버 중복 감지 ({attempt}회차) - 다른 뉴스 시도: {title[:30]}...")
                    continue
                
                # 실제 전송
                response = requests.post(
                    f"{SPRING_SERVER_URL}{endpoint}",
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code == 200:
                    logger.info(f"{source_name} 전송 성공 ({attempt}회차): {title[:30]}...")
                    return True
                else:
                    logger.error(f"{source_name} 전송 실패 ({attempt}회차): {response.status_code}")
                    
            except Exception as e:
                logger.error(f"{source_name} 전송 예외 ({attempt}회차): {e}")
        
        # 5회 재시도 후 실패
        logger.error(f"❌ {source_name} 최종 실패 - 5회 재시도 완료: {title[:50]}...")
        return False

# 전역 중복 체크 인스턴스
duplicate_checker = DuplicateChecker()