"""
실제 천문대 웹사이트에서 견학 일정 크롤링
"""
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

def crawl_gwacheon_science():
    """국립과천과학관 실제 프로그램 크롤링"""
    try:
        url = "https://www.sciencecenter.go.kr/scipia/program/program.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        programs = []
        # 실제 프로그램 목록 크롤링 시도
        for item in soup.select(".program-item, .event-item")[:3]:
            title_tag = item.select_one(".title, h3, h4")
            if title_tag:
                title = title_tag.get_text(strip=True)
                
                # 천체관측 관련 프로그램만 필터링
                if any(keyword in title for keyword in ['천체', '별', '우주', '천문']):
                    programs.append({
                        "title": title,
                        "description": f"국립과천과학관에서 운영하는 {title} 프로그램입니다.",
                        "schedule": "홈페이지 확인",
                        "fee": "홈페이지 확인",
                        "contact": "02-3677-1500",
                        "registration": "https://www.sciencecenter.go.kr"
                    })
        
        if programs:
            logger.info(f"국립과천과학관 실제 프로그램 {len(programs)}개 발견")
            return {
                "name": "국립과천과학관",
                "location": "경기도 과천시 상하벌로 110",
                "programs": programs
            }
        else:
            logger.info("국립과천과학관 천체관측 프로그램 없음")
            return None
            
    except Exception as e:
        logger.error(f"국립과천과학관 크롤링 실패: {e}")
        return None

def crawl_seoul_science():
    """서울시립과학관 실제 프로그램 크롤링"""
    try:
        url = "https://science.seoul.go.kr/program/list.do"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        programs = []
        for item in soup.select(".program-list li, .event-list li")[:3]:
            title_tag = item.select_one(".title, h3, h4, a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                
                if any(keyword in title for keyword in ['천체', '별', '우주', '천문']):
                    programs.append({
                        "title": title,
                        "description": f"서울시립과학관에서 운영하는 {title} 프로그램입니다.",
                        "schedule": "홈페이지 확인",
                        "fee": "홈페이지 확인", 
                        "contact": "02-970-4500",
                        "registration": "https://science.seoul.go.kr"
                    })
        
        if programs:
            logger.info(f"서울시립과학관 실제 프로그램 {len(programs)}개 발견")
            return {
                "name": "서울시립과학관",
                "location": "서울특별시 노원구 한글비석로 160",
                "programs": programs
            }
        else:
            logger.info("서울시립과학관 천체관측 프로그램 없음")
            return None
            
    except Exception as e:
        logger.error(f"서울시립과학관 크롤링 실패: {e}")
        return None

def crawl_kasi_programs():
    """한국천문연구원 견학 프로그램 크롤링"""
    try:
        url = "https://www.kasi.re.kr/kor/pageView/129"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, verify=False, timeout=15)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        programs = []
        # KASI 견학 프로그램 정보 크롤링
        for item in soup.select(".program-info, .visit-info")[:2]:
            title_tag = item.select_one("h3, h4, .title")
            if title_tag:
                title = title_tag.get_text(strip=True)
                programs.append({
                    "title": title,
                    "description": f"한국천문연구원 {title} 프로그램입니다.",
                    "schedule": "홈페이지 확인",
                    "fee": "무료",
                    "contact": "042-865-2195",
                    "registration": "https://www.kasi.re.kr"
                })
        
        if programs:
            logger.info(f"KASI 실제 프로그램 {len(programs)}개 발견")
            return {
                "name": "한국천문연구원",
                "location": "대전광역시 유성구 대덕대로 776",
                "programs": programs
            }
        else:
            logger.info("KASI 견학 프로그램 없음")
            return None
            
    except Exception as e:
        logger.error(f"KASI 프로그램 크롤링 실패: {e}")
        return None

def get_real_observatory_schedules() -> List[Dict]:
    """실제 천문대 웹사이트에서 크롤링한 일정만 반환"""
    real_observatories = []
    
    # 국립과천과학관
    gwacheon = crawl_gwacheon_science()
    if gwacheon:
        real_observatories.append(gwacheon)
    
    # 서울시립과학관
    seoul = crawl_seoul_science()
    if seoul:
        real_observatories.append(seoul)
    
    # 한국천문연구원
    kasi = crawl_kasi_programs()
    if kasi:
        real_observatories.append(kasi)
    
    logger.info(f"실제 크롤링된 천문대: {len(real_observatories)}개")
    return real_observatories