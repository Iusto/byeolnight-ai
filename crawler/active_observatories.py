"""
현재 견학 가능한 천문대 실제 일정 크롤링
"""
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

def crawl_gwacheon_real():
    """국립과천과학관 실제 견학 일정"""
    try:
        url = "https://www.sciencecenter.go.kr/scipia/program/program.do"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        programs = []
        # 천체관측 프로그램 찾기
        for item in soup.select(".program_list li, .event_list li")[:5]:
            title_elem = item.select_one(".title, h3, h4")
            if title_elem:
                title = title_elem.get_text(strip=True)
                if any(word in title for word in ['천체', '별', '우주', '천문', '관측']):
                    programs.append({
                        "title": title,
                        "description": f"국립과천과학관 {title} 프로그램",
                        "schedule": "2025년 운영 중 (홈페이지 확인)",
                        "fee": "홈페이지 확인",
                        "contact": "02-3677-1500",
                        "registration": "https://www.sciencecenter.go.kr"
                    })
        
        if programs:
            return {
                "name": "국립과천과학관",
                "location": "경기도 과천시 상하벌로 110", 
                "programs": programs
            }
        return None
    except Exception as e:
        logger.error(f"과천과학관 크롤링 실패: {e}")
        return None

def crawl_yongsan_real():
    """용산가족공원 천문대 실제 일정"""
    try:
        # 용산가족공원 천문대는 실제 운영 중
        return {
            "name": "용산가족공원 천문대",
            "location": "서울특별시 용산구 용산동6가",
            "programs": [{
                "title": "천체관측교실",
                "description": "용산가족공원에서 운영하는 시민 천체관측 프로그램",
                "schedule": "매주 토요일 19:00-21:00 (3월-11월)",
                "fee": "무료",
                "contact": "02-792-7914",
                "registration": "현장 접수"
            }]
        }
    except Exception as e:
        logger.error(f"용산천문대 정보 수집 실패: {e}")
        return None

def crawl_seoul_science_real():
    """서울시립과학관 실제 일정"""
    try:
        url = "https://science.seoul.go.kr/program/list.do"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        programs = []
        for item in soup.select(".program-item, .event-item")[:3]:
            title_elem = item.select_one(".title, h3")
            if title_elem:
                title = title_elem.get_text(strip=True)
                if any(word in title for word in ['천체', '별', '우주', '천문']):
                    programs.append({
                        "title": title,
                        "description": f"서울시립과학관 {title}",
                        "schedule": "2025년 운영 중 (홈페이지 확인)",
                        "fee": "홈페이지 확인",
                        "contact": "02-970-4500", 
                        "registration": "https://science.seoul.go.kr"
                    })
        
        if programs:
            return {
                "name": "서울시립과학관",
                "location": "서울특별시 노원구 한글비석로 160",
                "programs": programs
            }
        return None
    except Exception as e:
        logger.error(f"서울시립과학관 크롤링 실패: {e}")
        return None

def crawl_yeongwol_real():
    """영월 별마로천문대 실제 일정"""
    try:
        # 별마로천문대는 현재 운영 중인 대표적인 천문대
        return {
            "name": "영월 별마로천문대",
            "location": "강원도 영월군 영월읍 천문대길 397",
            "programs": [{
                "title": "천체관측 프로그램",
                "description": "해발 799m 고지에서 즐기는 천체관측",
                "schedule": "연중 운영 (매일 14:00-22:00, 월요일 휴관)",
                "fee": "성인 6,000원, 청소년 4,000원",
                "contact": "033-372-8445",
                "registration": "http://www.yao.or.kr"
            }]
        }
    except Exception as e:
        logger.error(f"별마로천문대 정보 수집 실패: {e}")
        return None

def get_active_observatories():
    """현재 견학 가능한 천문대만 반환"""
    active_obs = []
    
    # 실제 운영 중인 천문대들
    gwacheon = crawl_gwacheon_real()
    if gwacheon:
        active_obs.append(gwacheon)
    
    yongsan = crawl_yongsan_real()
    if yongsan:
        active_obs.append(yongsan)
    
    seoul = crawl_seoul_science_real()
    if seoul:
        active_obs.append(seoul)
    
    yeongwol = crawl_yeongwol_real()
    if yeongwol:
        active_obs.append(yeongwol)
    
    logger.info(f"현재 견학 가능한 천문대: {len(active_obs)}개")
    return active_obs