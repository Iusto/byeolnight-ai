"""
RSS 피드를 통한 실제 우주 뉴스 크롤링
"""
import feedparser
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict

logger = logging.getLogger(__name__)

def crawl_nasa_rss():
    """NASA RSS 피드에서 우주 뉴스 크롤링"""
    try:
        url = "https://www.nasa.gov/rss/dyn/breaking_news.rss"
        feed = feedparser.parse(url)
        
        articles = []
        for entry in feed.entries[:3]:  # 최신 3개만
            title = entry.title
            content = entry.summary if hasattr(entry, 'summary') else entry.description
            link = entry.link
            
            # 한국어 번역 (간단한 설명 추가)
            korean_content = f"NASA에서 발표한 우주 관련 뉴스입니다.\n\n원제: {title}\n\n{content[:200]}...\n\n🔗 원문 보기: {link}"
            
            articles.append({
                "title": f"[NASA] {title}",
                "content": korean_content,
                "source": "NASA_RSS"
            })
            
        logger.info(f"NASA RSS 뉴스 {len(articles)}개 처리 완료")
        return articles
        
    except Exception as e:
        logger.error(f"NASA RSS 크롤링 실패: {e}")
        return []

def crawl_esa_rss():
    """ESA(유럽우주국) RSS 피드에서 우주 뉴스 크롤링"""
    try:
        url = "https://www.esa.int/rssfeed/Our_Activities/Space_Science"
        feed = feedparser.parse(url)
        
        articles = []
        for entry in feed.entries[:2]:  # 최신 2개만
            title = entry.title
            content = entry.summary if hasattr(entry, 'summary') else entry.description
            link = entry.link
            
            korean_content = f"유럽우주국(ESA)에서 발표한 우주과학 뉴스입니다.\n\n원제: {title}\n\n{content[:200]}...\n\n🔗 원문 보기: {link}"
            
            articles.append({
                "title": f"[ESA] {title}",
                "content": korean_content,
                "source": "ESA_RSS"
            })
            
        logger.info(f"ESA RSS 뉴스 {len(articles)}개 처리 완료")
        return articles
        
    except Exception as e:
        logger.error(f"ESA RSS 크롤링 실패: {e}")
        return []

def crawl_spacenews_rss():
    """SpaceNews RSS 피드에서 우주 뉴스 크롤링"""
    try:
        url = "https://spacenews.com/feed/"
        feed = feedparser.parse(url)
        
        articles = []
        for entry in feed.entries[:2]:  # 최신 2개만
            title = entry.title
            content = entry.summary if hasattr(entry, 'summary') else entry.description
            link = entry.link
            
            korean_content = f"SpaceNews에서 보도한 우주산업 뉴스입니다.\n\n원제: {title}\n\n{content[:200]}...\n\n🔗 원문 보기: {link}"
            
            articles.append({
                "title": f"[SpaceNews] {title}",
                "content": korean_content,
                "source": "SpaceNews_RSS"
            })
            
        logger.info(f"SpaceNews RSS 뉴스 {len(articles)}개 처리 완료")
        return articles
        
    except Exception as e:
        logger.error(f"SpaceNews RSS 크롤링 실패: {e}")
        return []

def get_all_rss_news() -> List[Dict]:
    """모든 RSS 소스에서 뉴스 수집"""
    all_articles = []
    
    # NASA RSS
    all_articles.extend(crawl_nasa_rss())
    
    # ESA RSS  
    all_articles.extend(crawl_esa_rss())
    
    # SpaceNews RSS
    all_articles.extend(crawl_spacenews_rss())
    
    logger.info(f"RSS 뉴스 총 {len(all_articles)}개 수집 완료")
    return all_articles