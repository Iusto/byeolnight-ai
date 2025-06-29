import requests
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_observatory_schedules():
    """현재 견학 가능한 천문대 실제 일정만 반환"""
    try:
        from crawler.active_observatories import get_active_observatories
        active_schedules = get_active_observatories()
        
        if active_schedules:
            logger.info(f"견학 가능한 천문대: {len(active_schedules)}개")
            return active_schedules
        else:
            logger.warning("견학 가능한 천문대 없음")
            return []
    except Exception as e:
        logger.error(f"천문대 일정 수집 실패: {e}")
        return []

def send_schedule_to_spring(observatory: Dict, program: Dict) -> bool:
    """천문대 일정을 스프링 서버로 전송 (EVENT 카테고리)"""
    from config import SPRING_SERVER_URL, EVENT_API_KEY, REQUEST_TIMEOUT
    import requests
    
    event_data = {
        "title": f"[{observatory['name']}] {program['title']}",
        "content": program['description'],
        "location": observatory['location'],
        "eventDate": program['schedule'],
        "registrationUrl": program['registration'],
        "contact": program['contact'],
        "fee": program['fee'],
        "tags": ["천문대", "견학", "체험"],
        "source": observatory['name'],
        "url": program['registration'],
        "authorId": "observatorybot",
        "category": "EVENT",
        "type": "EVENT"
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-Crawler-API-Key": EVENT_API_KEY
    }
    
    try:
        response = requests.post(
            f"{SPRING_SERVER_URL}/api/admin/crawler/events",
            json=event_data,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"✅ {observatory['name']} 전송 성공")
            return True
        else:
            logger.error(f"❌ {observatory['name']} 전송 실패: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ {observatory['name']} 전송 예외: {e}")
        return False

async def crawl_observatory_schedules():
    """천문대 일정만 크롤링 (하루 1회: 오전 7시)"""
    logger.info(f"천문대 일정 크롤링 시작: {datetime.now()}")
    
    observatories = get_observatory_schedules()
    
    total_events = 0
    success_count = 0
    
    for observatory in observatories:
        for program in observatory['programs']:
            total_events += 1
            if send_schedule_to_spring(observatory, program):
                success_count += 1
    
    logger.info(f"천문대 일정 크롤링 완료: 총 {total_events}개 중 {success_count}개 전송 성공")
    
    return {
        "total_observatories": len(observatories),
        "total_events": total_events,
        "success": success_count,
        "observatories": [obs['name'] for obs in observatories]
    }