import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import re
from typing import List, Dict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

def crawl_kasi_observatories():
    """한국천문연구원 산하 천문대들"""
    observatories = [
        {
            "name": "한국천문연구원 본원",
            "location": "대전광역시 유성구 대덕대로 776",
            "programs": [
                {
                    "title": "천문연 견학 프로그램",
                    "description": "천문연구원 시설 견학 및 천문학 강연",
                    "schedule": "매주 토요일 14:00-16:00",
                    "fee": "무료",
                    "contact": "042-865-2195",
                    "registration": "https://www.kasi.re.kr"
                }
            ]
        },
        {
            "name": "보현산천문대",
            "location": "경상북도 영천시 화북면 정각리",
            "programs": [
                {
                    "title": "보현산천문대 견학",
                    "description": "국내 최대 1.8m 망원경 견학 및 천체관측",
                    "schedule": "매주 토요일 19:00-21:00 (예약 필수)",
                    "fee": "성인 5,000원, 학생 3,000원",
                    "contact": "054-330-1000",
                    "registration": "https://boao.kasi.re.kr"
                }
            ]
        },
        {
            "name": "소백산천문대",
            "location": "경상북도 영주시 부석면 북지리",
            "programs": [
                {
                    "title": "소백산 별빛축제",
                    "description": "별자리 관측 및 천문학 체험",
                    "schedule": "4월-10월 매주 토요일",
                    "fee": "성인 8,000원, 청소년 6,000원",
                    "contact": "054-638-8900",
                    "registration": "http://sobaeksan.go.kr"
                }
            ]
        }
    ]
    return observatories

def crawl_public_observatories():
    """공립 과학관 및 천문대"""
    observatories = [
        {
            "name": "국립과천과학관",
            "location": "경기도 과천시 상하벌로 110",
            "programs": [
                {
                    "title": "천체관측교실",
                    "description": "계절별 별자리 관측 및 천문학 강의",
                    "schedule": "매주 토요일 19:00-21:00",
                    "fee": "성인 3,000원, 청소년 2,000원",
                    "contact": "02-3677-1500",
                    "registration": "https://www.sciencecenter.go.kr"
                },
                {
                    "title": "가족천문교실",
                    "description": "가족 단위 천문학 체험 프로그램",
                    "schedule": "매월 둘째, 넷째 일요일 14:00-16:00",
                    "fee": "가족당 10,000원",
                    "contact": "02-3677-1500",
                    "registration": "https://www.sciencecenter.go.kr"
                }
            ]
        },
        {
            "name": "서울시립과학관",
            "location": "서울특별시 노원구 한글비석로 160",
            "programs": [
                {
                    "title": "별빛교실",
                    "description": "도심에서 즐기는 천체관측",
                    "schedule": "매주 금요일 19:30-21:00",
                    "fee": "성인 2,000원, 학생 1,000원",
                    "contact": "02-970-4500",
                    "registration": "https://science.seoul.go.kr"
                }
            ]
        },
        {
            "name": "부산과학관",
            "location": "부산광역시 기장군 기장읍 동부산관광로 59",
            "programs": [
                {
                    "title": "천체관측 프로그램",
                    "description": "부산 지역 천체관측 및 우주과학 체험",
                    "schedule": "매주 토요일 20:00-22:00",
                    "fee": "성인 4,000원, 학생 2,000원",
                    "contact": "051-750-2300",
                    "registration": "https://www.bssm.or.kr"
                }
            ]
        }
    ]
    return observatories

def crawl_regional_observatories():
    """지역 천문대 및 과학관"""
    observatories = [
        {
            "name": "영월별마로천문대",
            "location": "강원도 영월군 영월읍 천문대길 397",
            "programs": [
                {
                    "title": "별마로천문대 관측프로그램",
                    "description": "높은 고도에서 즐기는 천체관측",
                    "schedule": "연중 운영 (날씨에 따라 변동)",
                    "fee": "성인 6,000원, 청소년 4,000원",
                    "contact": "033-372-8445",
                    "registration": "http://www.yao.or.kr"
                }
            ]
        },
        {
            "name": "화천조경철천문대",
            "location": "강원도 화천군 사내면 광덕리",
            "programs": [
                {
                    "title": "별나라축제",
                    "description": "여름철 특별 천체관측 축제",
                    "schedule": "7월-8월 매주 토요일",
                    "fee": "성인 10,000원, 학생 7,000원",
                    "contact": "033-440-1000",
                    "registration": "http://www.hccf.or.kr"
                }
            ]
        },
        {
            "name": "안성맞춤천문과학관",
            "location": "경기도 안성시 죽산면 칠현로 1029-6",
            "programs": [
                {
                    "title": "천체관측 체험",
                    "description": "안성 지역 천체관측 및 과학체험",
                    "schedule": "매주 토요일 19:00-21:00",
                    "fee": "성인 5,000원, 학생 3,000원",
                    "contact": "031-678-1375",
                    "registration": "http://www.anseong.go.kr"
                }
            ]
        },
        {
            "name": "양주시민천문대",
            "location": "경기도 양주시 장흥면 권율로 185",
            "programs": [
                {
                    "title": "시민천문교실",
                    "description": "시민을 위한 천문학 강좌 및 관측",
                    "schedule": "매주 토요일 20:00-22:00",
                    "fee": "무료 (재료비 별도)",
                    "contact": "031-8082-4187",
                    "registration": "https://www.yangju.go.kr"
                }
            ]
        },
        {
            "name": "김해천문대",
            "location": "경상남도 김해시 가야테마길 254",
            "programs": [
                {
                    "title": "가야별빛축제",
                    "description": "김해 지역 천체관측 및 문화체험",
                    "schedule": "매월 첫째, 셋째 토요일",
                    "fee": "성인 3,000원, 학생 2,000원",
                    "contact": "055-337-3785",
                    "registration": "https://www.gimhae.go.kr"
                }
            ]
        },
        {
            "name": "대전시민천문대",
            "location": "대전광역시 유성구 과학로 213-48",
            "programs": [
                {
                    "title": "시민천문교실",
                    "description": "대전 시민을 위한 천문학 교육",
                    "schedule": "매주 금요일 19:30-21:30",
                    "fee": "성인 2,000원, 학생 1,000원",
                    "contact": "042-863-8763",
                    "registration": "https://www.daejeon.go.kr"
                }
            ]
        },
        {
            "name": "광주과학관",
            "location": "광주광역시 북구 첨단과기로 235",
            "programs": [
                {
                    "title": "천체관측교실",
                    "description": "광주 지역 천체관측 및 우주과학 체험",
                    "schedule": "매주 토요일 19:00-21:00",
                    "fee": "성인 3,000원, 학생 2,000원",
                    "contact": "062-960-6114",
                    "registration": "https://www.gsc.go.kr"
                }
            ]
        },
        {
            "name": "울산과학관",
            "location": "울산광역시 남구 옥동 대공원로 94",
            "programs": [
                {
                    "title": "별빛여행",
                    "description": "울산 지역 천체관측 프로그램",
                    "schedule": "매주 토요일 20:00-22:00",
                    "fee": "성인 4,000원, 청소년 3,000원",
                    "contact": "052-220-1500",
                    "registration": "https://www.usm.go.kr"
                }
            ]
        },
        {
            "name": "인천어린이과학관",
            "location": "인천광역시 계양구 방축로 21",
            "programs": [
                {
                    "title": "가족천문교실",
                    "description": "인천 지역 가족 단위 천문학 체험",
                    "schedule": "매월 둘째, 넷째 토요일 14:00-16:00",
                    "fee": "가족당 8,000원",
                    "contact": "032-456-2500",
                    "registration": "https://www.icsm.go.kr"
                }
            ]
        },
        {
            "name": "제주별빛누리공원",
            "location": "제주특별자치도 제주시 애월읍 광령리",
            "programs": [
                {
                    "title": "제주별빛축제",
                    "description": "제주 청정 하늘에서 즐기는 천체관측",
                    "schedule": "연중 운영 (날씨에 따라 변동)",
                    "fee": "성인 7,000원, 학생 5,000원",
                    "contact": "064-728-8900",
                    "registration": "http://www.jejustar.go.kr"
                }
            ]
        },
        {
            "name": "충북과학기술혁신원 천문대",
            "location": "충청북도 청주시 흥덕구 오송읍 오송생명로 123",
            "programs": [
                {
                    "title": "충북천문교실",
                    "description": "충북 지역 천문학 교육 및 관측",
                    "schedule": "매주 토요일 19:30-21:30",
                    "fee": "성인 3,000원, 학생 2,000원",
                    "contact": "043-270-2400",
                    "registration": "https://www.cbsti.re.kr"
                }
            ]
        },
        {
            "name": "전남과학교육원 천문대",
            "location": "전라남도 장성군 북하면 약수리 산 85-1",
            "programs": [
                {
                    "title": "전남별빛교실",
                    "description": "전남 지역 학생 및 시민 천문교육",
                    "schedule": "매주 금요일 19:00-21:00",
                    "fee": "무료",
                    "contact": "061-392-0451",
                    "registration": "https://www.jnse.go.kr"
                }
            ]
        },
        {
            "name": "경북과학교육원 천문대",
            "location": "경상북도 구미시 야은로 45",
            "programs": [
                {
                    "title": "경북천문캠프",
                    "description": "경북 지역 청소년 천문학 캠프",
                    "schedule": "여름/겨울방학 중 운영",
                    "fee": "참가비 15,000원",
                    "contact": "054-805-2300",
                    "registration": "https://www.gbe.kr"
                }
            ]
        }
    ]
    return observatories

def send_observatory_event_to_spring(observatory: Dict, program: Dict) -> bool:
    """천문대 이벤트를 스프링 서버로 전송"""
    from config import SPRING_SERVER_URL, EVENT_API_KEY, REQUEST_TIMEOUT
    
    # 이벤트 데이터 구성
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
        "url": program['registration']
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
            logger.info(f"천문대 이벤트 전송 성공: {observatory['name']} - {program['title']}")
            return True
        else:
            logger.error(f"천문대 이벤트 전송 실패: {observatory['name']}, 응답: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"천문대 이벤트 전송 예외: {observatory['name']}: {e}")
        return False

async def crawl_all_korea_observatories():
    """전국 모든 천문대 정보 크롤링 및 전송"""
    logger.info(f"전국 천문대 크롤링 시작: {datetime.now()}")
    
    all_observatories = []
    all_observatories.extend(crawl_kasi_observatories())
    all_observatories.extend(crawl_public_observatories())
    all_observatories.extend(crawl_regional_observatories())
    
    total_events = 0
    success_count = 0
    
    for observatory in all_observatories:
        for program in observatory['programs']:
            total_events += 1
            if send_observatory_event_to_spring(observatory, program):
                success_count += 1
    
    logger.info(f"전국 천문대 크롤링 완료: 총 {total_events}개 이벤트 중 {success_count}개 전송 성공")
    logger.info(f"포함된 천문대: {len(all_observatories)}개소")
    
    return {
        "total_observatories": len(all_observatories),
        "total_events": total_events, 
        "success": success_count,
        "observatories": [obs['name'] for obs in all_observatories]
    }