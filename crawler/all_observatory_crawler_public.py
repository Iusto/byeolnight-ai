import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import re
from typing import List, Dict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

def send_observatory_event_to_spring_public(observatory: Dict, program: Dict) -> bool:
    """천문대 이벤트를 Public 엔드포인트로 전송 (임시 해결책)"""
    from config import SPRING_SERVER_URL, REQUEST_TIMEOUT
    
    # 이벤트 내용을 뉴스 형태로 포맷팅
    formatted_content = f"""🏛️ **{observatory['name']} 이벤트**

🎯 **프로그램**: {program['title']}
📝 **설명**: {program['description']}
📅 **일정**: {program['schedule']}
📍 **위치**: {observatory['location']}
💰 **참가비**: {program['fee']}
📞 **문의**: {program['contact']}

---
🔗 **신청하기**: {program['registration']}
🏷️ **카테고리**: 천문대/이벤트"""

    payload = {
        "title": f"[{observatory['name']}] {program['title']}",
        "content": formatted_content,
        "type": "OBSERVATORY"
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(
            f"{SPRING_SERVER_URL}/api/public/ai/news",
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"천문대 이벤트 전송 성공 (Public): {observatory['name']} - {program['title']}")
            return True
        else:
            logger.error(f"천문대 이벤트 전송 실패 (Public): {observatory['name']}, 응답: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"천문대 이벤트 전송 예외 (Public): {observatory['name']}: {e}")
        return False

# 기존 천문대 데이터 함수들을 import
from crawler.all_observatory_crawler import (
    crawl_kasi_observatories,
    crawl_public_observatories, 
    crawl_regional_observatories
)

async def crawl_all_korea_observatories_public():
    """전국 모든 천문대 정보 크롤링 및 Public API로 전송"""
    logger.info(f"전국 천문대 크롤링 시작 (Public API): {datetime.now()}")
    
    all_observatories = []
    all_observatories.extend(crawl_kasi_observatories())
    all_observatories.extend(crawl_public_observatories())
    all_observatories.extend(crawl_regional_observatories())
    
    total_events = 0
    success_count = 0
    
    for observatory in all_observatories:
        for program in observatory['programs']:
            total_events += 1
            if send_observatory_event_to_spring_public(observatory, program):
                success_count += 1
    
    logger.info(f"전국 천문대 크롤링 완료 (Public API): 총 {total_events}개 이벤트 중 {success_count}개 전송 성공")
    logger.info(f"포함된 천문대: {len(all_observatories)}개소")
    
    return {
        "total_observatories": len(all_observatories),
        "total_events": total_events, 
        "success": success_count,
        "observatories": [obs['name'] for obs in all_observatories]
    }