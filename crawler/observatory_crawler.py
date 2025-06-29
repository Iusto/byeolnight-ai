import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import re
from typing import List, Dict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

def crawl_kasi_observatory():
    """한국천문연구원 천문대 견학 일정"""
    try:
        url = "https://www.kasi.re.kr/kor/pageView/174"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        events = []
        # 견학 일정 테이블에서 정보 추출
        for row in soup.select(".board_list tbody tr")[:5]:
            title_elem = row.select_one("td.subject a")
            date_elem = row.select_one("td:nth-child(3)")
            
            if title_elem and date_elem:
                title = title_elem.get_text(strip=True)
                date = date_elem.get_text(strip=True)
                
                events.append({
                    "name": "한국천문연구원",
                    "title": title,
                    "date": date,
                    "location": "대전 유성구",
                    "url": f"https://www.kasi.re.kr{title_elem.get('href')}",
                    "type": "견학"
                })
        
        return events
    except Exception as e:
        logger.error(f"KASI 천문대 크롤링 실패: {e}")
        return []

def crawl_seoul_observatory():
    """서울시립과학관 천문대 프로그램"""
    try:
        url = "https://science.seoul.go.kr/program/list"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        events = []
        for item in soup.select(".program-item")[:3]:
            title_elem = item.select_one(".title")
            date_elem = item.select_one(".date")
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                date = date_elem.get_text(strip=True) if date_elem else "일정 확인 필요"
                
                if "천문" in title or "별" in title or "우주" in title:
                    events.append({
                        "name": "서울시립과학관",
                        "title": title,
                        "date": date,
                        "location": "서울 노원구",
                        "url": url,
                        "type": "체험프로그램"
                    })
        
        return events
    except Exception as e:
        logger.error(f"서울시립과학관 크롤링 실패: {e}")
        return []

def crawl_gwacheon_observatory():
    """국립과천과학관 천문대 프로그램"""
    try:
        # 실제 사이트 구조에 맞게 조정 필요
        events = [
            {
                "name": "국립과천과학관",
                "title": "천체관측교실",
                "date": "매주 토요일 19:00-21:00",
                "location": "경기 과천시",
                "url": "https://www.sciencecenter.go.kr",
                "type": "정기프로그램"
            },
            {
                "name": "국립과천과학관",
                "title": "가족천문교실",
                "date": "매월 둘째, 넷째 일요일",
                "location": "경기 과천시",
                "url": "https://www.sciencecenter.go.kr",
                "type": "가족프로그램"
            }
        ]
        return events
    except Exception as e:
        logger.error(f"국립과천과학관 크롤링 실패: {e}")
        return []

def crawl_regional_observatories():
    """지역 천문대 정보"""
    observatories = [
        {
            "name": "보현산천문대",
            "title": "보현산천문대 견학프로그램",
            "date": "매주 토요일 (예약 필수)",
            "location": "경북 영천시",
            "url": "https://boao.kasi.re.kr",
            "type": "견학"
        },
        {
            "name": "소백산천문대",
            "title": "별빛축제 및 관측체험",
            "date": "4월-10월 매주 토요일",
            "location": "경북 영주시",
            "url": "http://sobaeksan.go.kr",
            "type": "체험"
        },
        {
            "name": "영월별마로천문대",
            "title": "별마로천문대 관측프로그램",
            "date": "연중 운영 (날씨에 따라 변동)",
            "location": "강원 영월군",
            "url": "http://www.yao.or.kr",
            "type": "관측"
        },
        {
            "name": "화천조경철천문대",
            "title": "별나라축제 및 천체관측",
            "date": "여름철 특별프로그램",
            "location": "강원 화천군",
            "url": "http://www.hccf.or.kr",
            "type": "축제"
        }
    ]
    return observatories

def send_observatory_to_spring(event: Dict) -> bool:
    """천문대 일정을 스프링 서버로 전송"""
    from config import SPRING_SERVER_URL, REQUEST_TIMEOUT
    
    # 천문대 일정 포맷팅
    formatted_content = f"""🏛️ **{event['name']} {event['type']}**

📅 **일정**: {event['date']}
📍 **위치**: {event['location']}
🎯 **프로그램**: {event['title']}

---
🔗 **자세한 정보**: {event['url']}
📞 **예약 문의**: 해당 천문대 홈페이지 참조
🏷️ **카테고리**: 천문대/견학"""

    payload = {
        "title": f"[{event['name']}] {event['title']}",
        "content": formatted_content,
        "type": "OBSERVATORY"
    }
    
    try:
        response = requests.post(
            f"{SPRING_SERVER_URL}/api/public/ai/news",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"천문대 일정 전송 성공: {event['name']}")
            return True
        else:
            logger.error(f"천문대 일정 전송 실패: {event['name']}, 응답: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"천문대 일정 전송 예외: {event['name']}: {e}")
        return False

async def crawl_all_observatories():
    """모든 천문대 일정 크롤링 및 전송"""
    logger.info(f"천문대 일정 크롤링 시작: {datetime.now()}")
    
    all_events = []
    all_events.extend(crawl_kasi_observatory())
    all_events.extend(crawl_seoul_observatory())
    all_events.extend(crawl_gwacheon_observatory())
    all_events.extend(crawl_regional_observatories())
    
    success_count = 0
    for event in all_events:
        if send_observatory_to_spring(event):
            success_count += 1
    
    logger.info(f"천문대 일정 크롤링 완료: 총 {len(all_events)}개 중 {success_count}개 전송 성공")
    return {"total": len(all_events), "success": success_count}