import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
from crawler.content_formatter import clean_and_format_content, extract_image_url

logger = logging.getLogger(__name__)

def extract_article_content(url: str) -> tuple[str, str]:
    """URL에서 실제 기사 내용과 이미지를 추출"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 이미지 추출
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        image_url = extract_image_url(soup, base_url)
        
        # 일반적인 기사 내용 선택자들
        content_selectors = [
            'article', '.article-content', '.post-content', '.entry-content',
            '.content', '.article-body', '.story-body', '.news-content',
            'main', '.main-content', '[role="main"]'
        ]
        
        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for elem in elements:
                    # 불필요한 태그 제거
                    for tag in elem.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                        tag.decompose()
                    
                    text = elem.get_text(separator=' ', strip=True)
                    if len(text) > 100:
                        content = text
                        break
                
                if content:
                    break
        
        # 내용이 없으면 전체 body에서 추출
        if not content:
            body = soup.find('body')
            if body:
                for tag in body.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                    tag.decompose()
                content = body.get_text(separator=' ', strip=True)
        
        # 내용 정리
        cleaned_content = clean_and_format_content(content) if content else "기사 내용을 가져올 수 없습니다."
        
        return cleaned_content, image_url or ""
        
    except Exception as e:
        logger.error(f"기사 내용 추출 실패 {url}: {e}")
        return "기사 내용을 가져올 수 없습니다.", ""

def extract_kasi_article(url: str) -> tuple[str, str]:
    """한국천문연구원 기사 내용 추출"""
    try:
        full_url = f"https://www.kasi.re.kr{url}" if url.startswith('/') else url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(full_url, headers=headers, timeout=15, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # KASI 사이트 특화 선택자
        content_elem = soup.select_one('.board_view .content, .view_content, .article_content')
        if content_elem:
            # 불필요한 태그 제거
            for tag in content_elem.find_all(['script', 'style']):
                tag.decompose()
            
            content = content_elem.get_text(separator=' ', strip=True)
            cleaned_content = clean_and_format_content(content)
            return cleaned_content, ""
        
        return extract_article_content(full_url)
        
    except Exception as e:
        logger.error(f"KASI 기사 추출 실패 {url}: {e}")
        return "기사 내용을 가져올 수 없습니다.", ""

def extract_sciencetimes_article(url: str) -> tuple[str, str]:
    """사이언스타임즈 기사 내용 추출"""
    try:
        full_url = url if url.startswith('http') else f"https://www.sciencetimes.co.kr{url}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(full_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 사이언스타임즈 특화 선택자
        content_elem = soup.select_one('.article-content, .entry-content, .post-content')
        if content_elem:
            for tag in content_elem.find_all(['script', 'style', 'div.ad']):
                tag.decompose()
            
            content = content_elem.get_text(separator=' ', strip=True)
            cleaned_content = clean_and_format_content(content)
            return cleaned_content, ""
        
        return extract_article_content(full_url)
        
    except Exception as e:
        logger.error(f"사이언스타임즈 기사 추출 실패 {url}: {e}")
        return "기사 내용을 가져올 수 없습니다.", ""