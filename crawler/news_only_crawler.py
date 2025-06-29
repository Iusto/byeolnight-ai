import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import urllib3
from crawler.content_extractor import extract_article_content, extract_kasi_article, extract_sciencetimes_article
from crawler.content_formatter import format_news_article
from translator.free_translator import smart_free_translate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logger = logging.getLogger(__name__)

def crawl_sciencetimes():
    """사이언스타임즈 - 대중 친화적 우주과학 뉴스"""
    try:
        # 우주/병계 카테고리 URL 수정
        url = "https://www.sciencetimes.co.kr/news/articleList.html?sc_section_code=S1N8&view_type=sm"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.content, "html.parser")

        articles = []
        # 사이언스타임즈 기사 리스트 셀렉터 수정
        for item in soup.select(".article-list-content")[:3]:
            title_tag = item.select_one(".titles a") or item.select_one("h4 a") or item.select_one(".article-list-titles a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                article_url = title_tag.get('href')
                
                if not article_url.startswith('http'):
                    article_url = "https://www.sciencetimes.co.kr" + article_url
                
                # 간단한 내용 추출
                content = f"사이언스타임즈에서 보도한 우주과학 뉴스입니다. {title}"
                
                articles.append({
                    "title": f"[사이언스타임즈] {title}",
                    "content": content + f"\n\n🔗 원문 보기: {article_url}",
                    "source": "ScienceTimes"
                })
                logger.info(f"사이언스타임즈 기사 처리 완료: {title[:50]}...")
        
        return articles
    except Exception as e:
        logger.error(f"사이언스타임즈 크롤링 실패: {e}")
        return []  # 실패 시 빈 리스트 반환

def crawl_kasi():
    """한국천문연구원 - 공식 발표 및 기술 자료"""
    try:
        url = "https://www.kasi.re.kr/kor/publication/pressRelease"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, verify=False, timeout=15)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        # KASI 보도자료 셀렉터 수정
        for item in soup.select(".board_list tbody tr")[:3]:
            title_tag = item.select_one("td.subject a") or item.select_one(".subject a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                article_url = title_tag.get('href')
                
                if not article_url.startswith('http'):
                    full_url = f"https://www.kasi.re.kr{article_url}"
                else:
                    full_url = article_url
                
                # 간단한 내용 생성
                content = f"한국천문연구원에서 발표한 공식 보도자료입니다. {title}"
                
                articles.append({
                    "title": f"[한국천문연구원] {title}",
                    "content": content + f"\n\n🔗 원문 보기: {full_url}",
                    "source": "KASI"
                })
                logger.info(f"KASI 기사 처리 완료: {title[:50]}...")
        
        return articles
    except Exception as e:
        logger.error(f"KASI 크롤링 실패: {e}")
        return []  # 실패 시 빈 리스트 반환

def crawl_dongascience():
    """동아사이언스 - 우주/천문 섹션"""
    try:
        url = "https://www.dongascience.com/news.php?idx=45"
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        for item in soup.select(".article_list .list_item")[:3]:
            title_tag = item.select_one(".tit a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                article_url = "https://www.dongascience.com" + title_tag.get('href')
                
                full_content, image_url = extract_article_content(article_url)
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

def crawl_gwacheon_news():
    """국립과천과학관 뉴스 (실제 크롤링 구현 필요)"""
    try:
        # TODO: 실제 과천과학관 뉴스 페이지 크롤링 구현
        # 현재는 빈 리스트 반환
        logger.info("국립과천과학관 뉴스 크롤링 미구현")
        return []
    except Exception as e:
        logger.error(f"국립과천과학관 뉴스 크롤링 실패: {e}")
        return []

def send_news_to_spring(title: str, content: str, source: str) -> bool:
    """뉴스를 스프링 서버로 전송 (NEWS 카테고리)"""
    from utils.simple_sender import send_to_spring
    
    if len(content) > 2000:
        content = content[:1997] + "..."
    
    payload = {
        "title": title, 
        "content": content,
        "type": "NEWS",
        "authorId": "newsbot",
        "category": "NEWS",
        "source": source
    }
    
    return send_to_spring(payload, "/api/public/ai/news", source)

async def crawl_news_only():
    """우주 뉴스만 크롤링 (하루 2회: 오전 6시, 오후 12시)"""
    logger.info(f"우주 뉴스 크롤링 시작: {datetime.now()}")
    
    all_articles = []
    
    # 한국인 맞춤 우주 뉴스
    try:
        from crawler.korean_space_news import get_korean_space_news
        korean_articles = get_korean_space_news()
        all_articles.extend(korean_articles)
        logger.info(f"한국 우주 뉴스 {len(korean_articles)}개 수집")
    except Exception as e:
        logger.error(f"한국 우주 뉴스 크롤링 실패: {e}")
    
    # 기존 소스도 유지
    all_articles.extend(crawl_sciencetimes())
    all_articles.extend(crawl_kasi())
    
    # 백업 뉴스 (크롤링이 안될 때)
    if len(all_articles) == 0:
        try:
            from crawler.simple_news import get_simple_space_news
            backup_articles = get_simple_space_news()
            all_articles.extend(backup_articles)
            logger.info(f"백업 뉴스 {len(backup_articles)}개 사용")
        except Exception as e:
            logger.error(f"백업 뉴스 로드 실패: {e}")
    
    success_count = 0
    for article in all_articles:
        if send_news_to_spring(article["title"], article["content"], article["source"]):
            success_count += 1
    
    logger.info(f"우주 뉴스 크롤링 완료: 총 {len(all_articles)}개 중 {success_count}개 전송 성공")
    
    return {
        "total": len(all_articles), 
        "success": success_count,
        "sources": ["YTN사이언스", "조선일보", "사이언스온", "사이언스타임즈", "KASI"]
    }