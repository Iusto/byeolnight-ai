import logging
from datetime import datetime

logger = logging.getLogger(__name__)



def send_news_to_spring(title: str, content: str, source: str) -> bool:
    """뉴스를 스프링 서버로 전송 (Admin API)"""
    from utils.simple_sender import send_to_spring_admin
    
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
    
    return send_to_spring_admin(payload, "/api/admin/crawler/news", source)

async def crawl_news_only():
    """우주 뉴스만 크롤링 (하루 2회: 오전 6시, 오후 12시) - 5개 사이트 중 랜덤 선택"""
    logger.info(f"우주 뉴스 크롤링 시작: {datetime.now()}")
    
    all_articles = []
    selected_site = "없음"
    
    # 최적화된 뉴스 크롤링 사용
    try:
        from crawler.optimized_news_crawler import get_optimized_space_news
        articles = get_optimized_space_news()
        all_articles.extend(articles)
        selected_site = "최신뉴스크롤링"
        logger.info(f"최신 뉴스 크롤링에서 {len(articles)}개 뉴스 수집")
    except Exception as e:
        logger.error(f"뉴스 크롤링 실패: {e}")
        selected_site = "실패"
    
    # DB 기반 중복 체크 및 필터링
    try:
        from utils.duplicate_checker import filter_duplicate_articles
        filtered_articles = filter_duplicate_articles(all_articles)
        logger.info(f"중복 필터링: {len(all_articles)}개 → {len(filtered_articles)}개")
        all_articles = filtered_articles
    except Exception as e:
        logger.error(f"중복 체크 실패: {e}")
    
    # 스프링 서버로 전송 (중복 제거된 기사만)
    success_count = 0
    for article in all_articles:
        if send_news_to_spring(article["title"], article["content"], article["source"]):
            success_count += 1
    
    logger.info(f"우주 뉴스 크롤링 완료: 총 {len(all_articles)}개 중 {success_count}개 전송 성공")
    
    return {
        "total": len(all_articles), 
        "success": success_count,
        "selected_site": selected_site,
        "sources": ["구글뉴스RSS", "최신뉴스필터링"]
    }