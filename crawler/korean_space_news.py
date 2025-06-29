"""
한국인이 흥미로워할 우주 뉴스 크롤링
"""
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def crawl_ytn_science():
    """YTN 사이언스 - 우주/항공 뉴스"""
    try:
        url = "https://science.ytn.co.kr/program/program_view.php?s_mcd=0082&s_hcd="
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        for item in soup.select(".list_cont li")[:3]:
            title_tag = item.select_one("a")
            if title_tag and any(word in title_tag.text for word in ['우주', '로켓', '위성', '달', '화성', '천문']):
                title = title_tag.get_text(strip=True)
                link = "https://science.ytn.co.kr" + title_tag.get('href')
                
                articles.append({
                    "title": f"[YTN사이언스] {title}",
                    "content": f"YTN 사이언스에서 보도한 우주 관련 뉴스입니다.\n\n{title}\n\n🔗 원문: {link}",
                    "source": "YTN_Science"
                })
        
        logger.info(f"YTN 사이언스 뉴스 {len(articles)}개 수집")
        return articles
    except Exception as e:
        logger.error(f"YTN 사이언스 크롤링 실패: {e}")
        return []

def crawl_chosun_science():
    """조선일보 사이언스 - 우주 뉴스"""
    try:
        url = "https://www.chosun.com/science-health/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        for item in soup.select("article, .story-card")[:5]:
            title_tag = item.select_one("h3 a, .headline a, a")
            if title_tag and any(word in title_tag.text for word in ['우주', '로켓', '위성', '달', '화성', '천문', 'NASA', '스페이스X']):
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href')
                if not link.startswith('http'):
                    link = "https://www.chosun.com" + link
                
                articles.append({
                    "title": f"[조선일보] {title}",
                    "content": f"조선일보에서 보도한 우주 관련 뉴스입니다.\n\n{title}\n\n🔗 원문: {link}",
                    "source": "Chosun_Science"
                })
        
        logger.info(f"조선일보 사이언스 뉴스 {len(articles)}개 수집")
        return articles
    except Exception as e:
        logger.error(f"조선일보 사이언스 크롤링 실패: {e}")
        return []

def crawl_hani_science():
    """한겨레 사이언스온 - 우주 뉴스"""
    try:
        url = "http://scienceon.hani.co.kr/category/astronomy"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        
        articles = []
        for item in soup.select(".article-list li, .post")[:3]:
            title_tag = item.select_one("h3 a, .title a, a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href')
                if not link.startswith('http'):
                    link = "http://scienceon.hani.co.kr" + link
                
                articles.append({
                    "title": f"[사이언스온] {title}",
                    "content": f"한겨레 사이언스온에서 보도한 천문학 뉴스입니다.\n\n{title}\n\n🔗 원문: {link}",
                    "source": "ScienceOn"
                })
        
        logger.info(f"사이언스온 뉴스 {len(articles)}개 수집")
        return articles
    except Exception as e:
        logger.error(f"사이언스온 크롤링 실패: {e}")
        return []

def get_korean_space_news():
    """한국인 맞춤 우주 뉴스 수집"""
    all_articles = []
    
    all_articles.extend(crawl_ytn_science())
    all_articles.extend(crawl_chosun_science()) 
    all_articles.extend(crawl_hani_science())
    
    logger.info(f"한국 우주 뉴스 총 {len(all_articles)}개 수집")
    return all_articles