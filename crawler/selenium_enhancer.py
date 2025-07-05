#!/usr/bin/env python3
"""
Selenium을 사용한 기사 내용 품질 개선
"""
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def enhance_article_with_selenium(url: str, title: str) -> Tuple[str, str]:
    """Selenium으로 실제 기사 내용과 이미지 추출 (강화버전)"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from bs4 import BeautifulSoup
        import time
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        logger.info(f"Selenium으로 기사 내용 개선 시작: {url[:50]}...")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get(url)
        time.sleep(5)
        
        final_url = driver.current_url
        
        if 'news.google.com' not in final_url:
            logger.info(f"실제 사이트 도달: {final_url[:50]}...")
            
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            content_selectors = [
                '.article_body', '.news_body', '.view_body',
                '.article_txt', '.news_txt', '.view_txt',
                '.article_content', '.news_content', '.view_content',
                '.article-content', '.news-content', '.view-content',
                '.content_area', '.txt_area', '.article_area',
                '.article_body_contents', '.view_con_t',
                'article', '.content', '#content', '.main-content',
                '.post-content', '.entry-content', '.story-content',
                '.article-body', '.news-body', '.text-content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    for unwanted in element.select('script, style, .ad, .advertisement, .social, .share, .comment'):
                        unwanted.decompose()
                    
                    text = element.get_text(separator='\n', strip=True)
                    
                    if (len(text) > 300 and 
                        not any(skip in text.lower() for skip in ['광고', '구독', '로그인', '댓글', '공유하기', '카카오톡']) and
                        text.count('\n') >= 3):
                        
                        lines = text.split('\n')
                        unique_lines = []
                        seen_lines = set()
                        
                        for line in lines:
                            line = line.strip()
                            if (len(line) > 20 and 
                                line not in seen_lines and
                                not any(skip in line for skip in ['저작권', '무단전재', '사진=', '기자=', '출처='])):
                                unique_lines.append(line)
                                seen_lines.add(line)
                        
                        if len(unique_lines) >= 3:
                            content = '\n\n'.join(unique_lines[:8])
                            break
                
                if content:
                    break
            
            image_url = ""
            img_selectors = [
                "meta[property='og:image']",
                "meta[name='twitter:image']",
                "meta[property='twitter:image']",
                ".article_body img[src]",
                ".news_body img[src]",
                ".article-content img[src]",
                "article img[src]",
                ".content img[src]",
                "img[src]"
            ]
            
            for selector in img_selectors:
                if 'meta' in selector:
                    meta_img = soup.select_one(selector)
                    if meta_img and meta_img.get('content'):
                        src = meta_img.get('content')
                        if src and src.startswith('http') and any(ext in src.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
                            image_url = src
                            break
                else:
                    img = soup.select_one(selector)
                    if img and img.get('src'):
                        src = img.get('src')
                        if src and (src.startswith('http') or src.startswith('/')):
                            if not src.startswith('http'):
                                from urllib.parse import urljoin
                                src = urljoin(final_url, src)
                            if any(ext in src.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
                                image_url = src
                                break
            
            driver.quit()
            
            if content and len(content) > 500:
                logger.info(f"Selenium 성공: {len(content)}자 추출")
                return content[:2000], image_url
            else:
                logger.warning(f"Selenium 결과 부족: {len(content) if content else 0}자")
                return content if content else "", image_url
        else:
            logger.warning("구글 뉴스에서 벗어나지 못함")
            driver.quit()
            return "", ""
            
    except ImportError:
        logger.warning("Selenium 미설치 - pip install selenium 필요")
        return "", ""
    except Exception as e:
        logger.error(f"Selenium 오류: {e}")
        try:
            driver.quit()
        except:
            pass
        return "", ""

def is_selenium_available() -> bool:
    """Selenium 사용 가능 여부 확인"""
    try:
        from selenium import webdriver
        return True
    except ImportError:
        return False