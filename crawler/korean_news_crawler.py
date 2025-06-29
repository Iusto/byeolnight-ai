import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import urllib3
from crawler.content_extractor import extract_article_content, extract_kasi_article, extract_sciencetimes_article
from crawler.content_formatter import format_news_article
from translator.free_translator import smart_free_translate
from crawler.all_observatory_crawler import crawl_all_korea_observatories

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

def crawl_sciencetimes():
    """사이언스타임즈 - 대중 친화적 우주과학 뉴스"""
    try:
        url = "https://www.sciencetimes.co.kr/news/category/%ec%9a%b0%ec%a3%bc%eb%b3%91%ea%b3%84"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")

        articles = []
        for item in soup.select("ul.article-list li")[:3]:
            title_tag = item.select_one("h4 a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                article_url = title_tag.get('href')
                
                # 실제 기사 내용과 이미지 추출
                full_content, image_url = extract_sciencetimes_article(article_url)
                
                # 기사 포맷팅
                formatted_title, formatted_content = format_news_article(
                    title, full_content, "사이언스타임즈", article_url, image_url
                )
                
                articles.append({
                    "title": formatted_title,
                    "content": formatted_content,
                    "source": "ScienceTimes"
                })
                logger.info(f"사이언스타임즈 기사 처리 완료: {title[:50]}...")
        return articles
    except Exception as e:
        logger.error(f"사이언스타임즈 크롤링 실패: {e}")
        return []

def crawl_kasi():
    """한국천문연구원 - 공식 발표 및 기술 자료"""
    try:
        url = "https://www.kasi.re.kr/kor/publication/pressRelease"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        for item in soup.select(".board_list tbody tr")[:3]:
            title_tag = item.select_one("td.subject a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                article_url = title_tag.get('href')
                full_url = f"https://www.kasi.re.kr{article_url}"
                
                # 실제 기사 내용 추출
                full_content, image_url = extract_kasi_article(article_url)
                
                # 기사 포맷팅
                formatted_title, formatted_content = format_news_article(
                    title, full_content, "한국천문연구원", full_url, image_url
                )
                
                articles.append({
                    "title": formatted_title,
                    "content": formatted_content,
                    "source": "KASI"
                })
                logger.info(f"KASI 기사 처리 완료: {title[:50]}...")
        return articles
    except Exception as e:
        logger.error(f"KASI 크롤링 실패: {e}")
        return []

def crawl_dongascience():
    """동아사이언스 - 우주/천문 섹션"""
    try:
        url = "https://www.dongascience.com/news.php?idx=45"  # 우주/천문 카테고리
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        for item in soup.select(".article_list .list_item")[:3]:
            title_tag = item.select_one(".tit a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                article_url = "https://www.dongascience.com" + title_tag.get('href')
                
                # 실제 기사 내용 추출
                full_content, image_url = extract_article_content(article_url)
                
                # 기사 포맷팅
                formatted_title, formatted_content = format_news_article(
                    title, full_content, "동아사이언스", article_url, image_url
                )
                
                articles.append({
                    "title": formatted_title,
                    "content": formatted_content,
                    "source": "DongaScience"
                })
                logger.info(f"동아사이언스 기사 처리 완료: {title[:50]}...")
        return articles
    except Exception as e:
        logger.error(f"동아사이언스 크롤링 실패: {e}")
        return []

def crawl_science_museums():
    """과학관 및 천문대 이벤트 정보"""
    try:
        events = []
        
        # 국립과천과학관 프로그램
        gwacheon_events = [
            {
                "name": "국립과천과학관",
                "title": "천체관측교실 - 겨울철 별자리 관측",
                "date": "매주 토요일 19:00-21:00",
                "location": "경기 과천시",
                "content": "겨울철 대표 별자리와 행성을 망원경으로 직접 관측하는 프로그램입니다. 가족 단위 참여 가능하며, 날씨에 따라 실내 천문학 강의로 대체됩니다.",
                "url": "https://www.sciencecenter.go.kr"
            },
            {
                "name": "국립과천과학관",
                "title": "가족천문교실 - 우주탐사 이야기",
                "date": "매월 둘째, 넷째 일요일 14:00-16:00",
                "location": "경기 과천시",
                "content": "최신 우주탐사 소식과 함께 간단한 망원경 만들기 체험을 진행합니다. 초등학생 이상 참여 가능합니다.",
                "url": "https://www.sciencecenter.go.kr"
            }
        ]
        
        # 지역 천문대 특별 프로그램
        regional_events = [
            {
                "name": "영월별마로천문대",
                "title": "겨울 별축제 - 오리온자리 대탐험",
                "date": "12월-2월 매주 금,토요일",
                "location": "강원 영월군",
                "content": "겨울철 가장 아름다운 오리온자리와 주변 천체들을 대형 망원경으로 관측합니다. 별빛 사진 촬영 체험도 함께 진행됩니다.",
                "url": "http://www.yao.or.kr"
            },
            {
                "name": "보현산천문대",
                "title": "천문대 견학 및 관측체험",
                "date": "매주 토요일 (예약 필수)",
                "location": "경북 영천시",
                "content": "국내 최대 규모의 1.8m 망원경 견학과 함께 실제 천체 관측을 체험할 수 있습니다. 중학생 이상 권장합니다.",
                "url": "https://boao.kasi.re.kr"
            }
        ]
        
        all_events = gwacheon_events + regional_events
        
        for event in all_events:
            formatted_content = f"""🏛️ **{event['name']} 특별 프로그램**

🎯 **프로그램**: {event['title']}
📅 **일정**: {event['date']}
📍 **위치**: {event['location']}

📝 **프로그램 소개**
{event['content']}

---
🔗 **자세한 정보**: {event['url']}
📞 **예약 문의**: 해당 기관 홈페이지 참조
🏷️ **카테고리**: 천문대/체험프로그램"""

            events.append({
                "title": f"[{event['name']}] {event['title']}",
                "content": formatted_content,
                "source": "Observatory"
            })
        
        logger.info(f"과학관/천문대 이벤트 {len(events)}개 처리 완료")
        return events
        
    except Exception as e:
        logger.error(f"과학관/천문대 이벤트 크롤링 실패: {e}")
        return []

def send_to_spring_server(title: str, content: str, content_type: str = "NEWS"):
    """스프링 서버로 콘텐츠 전송"""
    from config import SPRING_SERVER_URL, REQUEST_TIMEOUT
    
    # content 길이 제한 (2000자)
    if len(content) > 2000:
        content = content[:1997] + "..."
    
    payload = {
        "title": title, 
        "content": content,
        "type": content_type
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        # Public 엔드포인트 사용 (JWT 인증 불필요)
        response = requests.post(
            f"{SPRING_SERVER_URL}/api/public/ai/news",
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            logger.info(f"전송 성공: {title[:50]}...")
            return True
        else:
            logger.error(f"전송 실패: {title[:30]}..., 응답 코드: {response.status_code}, 응답: {response.text}")
            return False
    except requests.exceptions.Timeout:
        logger.error(f"전송 타임아웃: {title[:30]}...")
        return False
    except requests.exceptions.ConnectionError:
        logger.error(f"연결 오류: {title[:30]}... - 스프링 서버가 실행 중인지 확인하세요")
        return False
    except Exception as e:
        logger.error(f"전송 예외: {title[:30]}...: {e}")
        return False

async def crawl_all_korean_content():
    """모든 한국 뉴스 소스와 전국 천문대에서 크롤링하여 스프링 서버로 전송"""
    logger.info(f"한국 콘텐츠 크롤링 시작: {datetime.now()}")
    
    # 1. 뉴스 크롤링
    all_articles = []
    all_articles.extend(crawl_sciencetimes())
    all_articles.extend(crawl_kasi())
    all_articles.extend(crawl_dongascience())
    
    # 2. 과학관 이벤트 크롤링
    observatory_events = crawl_science_museums()
    
    # 3. 전국 천문대 크롤링 (새로운 이벤트 API 사용)
    korea_observatories_result = await crawl_all_korea_observatories()
    
    # 뉴스 전송
    news_success = 0
    for article in all_articles:
        if send_to_spring_server(article["title"], article["content"], "NEWS"):
            news_success += 1
    
    # 과학관 이벤트 전송 (기존 방식)
    observatory_success = 0
    for event in observatory_events:
        if send_to_spring_server(event["title"], event["content"], "OBSERVATORY"):
            observatory_success += 1
    
    total_items = len(all_articles) + len(observatory_events) + korea_observatories_result["total_events"]
    total_success = news_success + observatory_success + korea_observatories_result["success"]
    
    logger.info(f"한국 콘텐츠 크롤링 완료: 총 {total_items}개 중 {total_success}개 전송 성공")
    logger.info(f"  - 뉴스: {len(all_articles)}개 중 {news_success}개 성공")
    logger.info(f"  - 과학관 이벤트: {len(observatory_events)}개 중 {observatory_success}개 성공")
    logger.info(f"  - 전국 천문대: {korea_observatories_result['total_events']}개 중 {korea_observatories_result['success']}개 성공")
    
    return {
        "total": total_items, 
        "success": total_success,
        "news": {"total": len(all_articles), "success": news_success},
        "science_museums": {"total": len(observatory_events), "success": observatory_success},
        "korea_observatories": korea_observatories_result
    }