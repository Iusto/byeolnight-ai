#!/usr/bin/env python3
"""
최적화된 우주 뉴스 크롤링 (날짜 필터링 포함)
"""
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
from dateutil import parser
import re

logger = logging.getLogger(__name__)

def is_recent_news(pub_date_str, max_days=7):
    """뉴스가 최근 N일 이내인지 확인"""
    try:
        if not pub_date_str:
            return True  # 날짜 정보가 없으면 포함
        
        # 다양한 날짜 형식 파싱
        pub_date = parser.parse(pub_date_str)
        cutoff_date = datetime.now() - timedelta(days=max_days)
        
        return pub_date.replace(tzinfo=None) >= cutoff_date
    except:
        return True  # 파싱 실패시 포함

def is_valid_content(title, content):
    """유효한 뉴스 콘텐츠인지 확인"""
    if not title or len(title.strip()) < 10:
        return False
    if content and len(content.strip()) < 20:
        return False
    return True

def crawl_google_news_optimized():
    """최적화된 구글 뉴스 크롤링"""
    try:
        import random
        import time
        
        # 캐시 방지를 위한 랜덤 파라미터 추가
        cache_buster = int(time.time()) + random.randint(1, 1000)
        url = f"https://news.google.com/rss/search?q=우주+뉴스&hl=ko&gl=KR&ceid=KR:ko&_cb={cache_buster}"
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100,120)}.0.0.0 Safari/537.36',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.content, "xml")
        
        articles = []
        seen_titles = set()  # 중복 제거용
        
        for item in soup.find_all("item")[:10]:
            title_tag = item.find("title")
            link_tag = item.find("link")
            source_tag = item.find("source")
            pub_date_tag = item.find("pubDate")
            
            if not title_tag:
                continue
                
            title = title_tag.get_text(strip=True)
            pub_date = pub_date_tag.get_text(strip=True) if pub_date_tag else ""
            
            # 날짜 필터링 (최근 7일)
            if not is_recent_news(pub_date, max_days=7):
                logger.debug(f"오래된 뉴스 제외: {title[:30]}...")
                continue
            
            # 제목에서 출처 완전 제거 (예: [한국대학신문], - 한국대학신문 등)
            clean_title = re.sub(r'^\[.*?\]\s*', '', title).strip()
            clean_title = re.sub(r'\s*-\s*[가-힣A-Za-z0-9\s]+$', '', clean_title).strip()
            
            # 중복 제거
            if clean_title in seen_titles:
                continue
            seen_titles.add(clean_title)
            
            link = link_tag.get_text(strip=True) if link_tag else ""
            source = source_tag.get_text(strip=True) if source_tag else "구글뉴스"
            
            # 상세 내용 추출
            content, image_url = get_article_content(link)
            
            # 무의미한 콘텐츠 필터링
            if content and any(skip_text in content for skip_text in [
                'Google 뉴스가 전세계', '전세계 매체로부터', 
                '종합한 최신 뉴스', '뉴스 소스', '뉴스 제공업체'
            ]):
                content = ""  # 무의미한 콘텐츠 제거
            
            # 콘텐츠 유효성 검사 (너무 엄격하지 않게)
            if not clean_title or len(clean_title.strip()) < 5:
                logger.debug(f"유효하지 않은 제목 제외: {title[:30]}...")
                continue
            
            # AI 평가 및 요약
            from ai.news_evaluator import evaluate_news_article
            evaluation = evaluate_news_article(clean_title, content, link)
            
            if evaluation["evaluation"] == "REJECT":
                logger.debug(f"AI 평가 거부: {title[:30]}... - {evaluation.get('reason', '')}")
                continue
            
            # 풍부한 콘텐츠 생성
            full_content = f"{source}에서 보도한 우주 관련 최신 뉴스입니다.\n\n"
            
            # AI 요약 추가
            if evaluation.get("summary") and len(evaluation["summary"]) > 20:
                full_content += f"🤖 AI 요약: {evaluation['summary']}\n\n"
            
            # 실제 기사 내용 추가 (더 자세히)
            if content and len(content.strip()) > 100:
                # 전체 내용을 적절히 요약해서 표시
                content_preview = content[:500] + "..." if len(content) > 500 else content
                full_content += f"📰 기사 내용:\n{content_preview}\n\n"
            elif content and len(content.strip()) > 50:
                full_content += f"📰 기사 요약: {content}\n\n"
            
            # 이미지 추가
            if image_url:
                full_content += f"🖼️ 관련 이미지: {image_url}\n\n"
            
            if pub_date:
                full_content += f"📅 발행일: {pub_date}\n"
            
            # AI 키워드 추가
            if evaluation.get("keywords") and len(evaluation["keywords"]) > 0:
                keywords_str = ", ".join(evaluation["keywords"][:3])
                full_content += f"🏷️ 핵심 키워드: {keywords_str}\n"
            
            full_content += f"🔗 원문 링크: {link}\n🌌 출처: {source}"
            
            articles.append({
                "title": clean_title,
                "content": full_content,
                "source": "GoogleNews",
                "published_at": pub_date,
                "url": link,
                "ai_evaluation": evaluation
            })
            
            if len(articles) >= 5:  # 최대 5개
                break
        
        logger.info(f"구글 뉴스 최신 우주 뉴스 {len(articles)}개 수집")
        return articles
        
    except Exception as e:
        logger.error(f"구글 뉴스 크롤링 실패: {e}")
        return []

def get_article_content(url):
    """기사 URL에서 상세 내용 추출 (강화버전)"""
    try:
        import time
        
        # 구글 뉴스 리다이렉트 처리 강화
        if 'news.google.com' in url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
                'Referer': 'https://news.google.com/'
            }
            
            # 단계별 리다이렉트 추적
            for attempt in range(3):
                try:
                    resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                    if resp.url != url and 'news.google.com' not in resp.url:
                        url = resp.url
                        logger.info(f"실제 기사 URL 발견: {url[:100]}...")
                        break
                    time.sleep(1)
                except:
                    continue
        
        # 강화된 헤더
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Cache-Control': 'no-cache'
        }
        
        resp = requests.get(url, headers=headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.content, "html.parser")
        
        # 광고/노이즈 제거
        for unwanted in soup.select('script, style, nav, header, footer, .ad, .advertisement, .social-share'):
            unwanted.decompose()
        
        # 한국 언론사 특화 셀렉터 (우선순위)
        content_selectors = [
            # 주요 한국 언론사
            ".article_body p", ".news_body p", ".article-body p", ".news-body p",
            ".view_content p", ".article_view p", ".news_view p",
            "#article_body p", "#news_body p", "#content p",
            ".content_area p", ".article_content p", ".news_content p",
            # 일반적인 셀렉터
            "article p", ".article-content p", ".post-content p",
            ".entry-content p", ".story-body p", ".article-text p",
            # 백업 셀렉터
            "main p", ".main-content p", "[class*='content'] p",
            "div p", "section p"
        ]
        
        content = ""
        for selector in content_selectors:
            paragraphs = soup.select(selector)
            if len(paragraphs) >= 2:  # 최소 2개 문단 이상
                valid_paragraphs = []
                for p in paragraphs[:8]:  # 최대 8개 문단
                    text = p.get_text(strip=True)
                    # 더 엄격한 필터링
                    if (len(text) > 30 and 
                        not any(skip in text.lower() for skip in [
                            '광고', '구독', '로그인', '회원가입', '댓글', '공유하기',
                            '이메일', '페이스북', '트위터', '카카오톡', '라인',
                            'copyright', 'ⓒ', '©', '저작권', '무단전재'
                        ]) and
                        not text.startswith(('사진=', '이미지=', '출처=', '기자='))):
                        valid_paragraphs.append(text)
                
                if len(valid_paragraphs) >= 2:
                    content = "\n\n".join(valid_paragraphs[:5])  # 최대 5개 문단
                    logger.info(f"기사 내용 추출 성공: {len(content)}자")
                    break
        
        # 본문이 없으면 메타 설명 사용
        if not content or len(content) < 100:
            meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
            if meta_desc and meta_desc.get('content'):
                desc = meta_desc.get('content').strip()
                if len(desc) > 50:
                    content = desc
                    logger.info(f"메타 설명에서 내용 추출: {len(content)}자")
        
        # 이미지 추출 강화
        image_url = ""
        img_selectors = [
            # 메타 태그 우선
            "meta[property='og:image']", "meta[name='twitter:image']",
            # 기사 내 이미지
            ".article_body img[src]", ".news_body img[src]", ".article-body img[src]",
            ".view_content img[src]", ".article_view img[src]", ".content img[src]",
            "article img[src]", ".article-content img[src]", "main img[src]"
        ]
        
        for selector in img_selectors:
            if 'meta' in selector:
                meta_img = soup.select_one(selector)
                if meta_img and meta_img.get('content'):
                    src = meta_img.get('content')
                    if src and (src.startswith('http') or src.startswith('/')):
                        if not src.startswith('http'):
                            from urllib.parse import urljoin
                            src = urljoin(url, src)
                        if any(ext in src.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp', '.gif']):
                            image_url = src
                            logger.info(f"이미지 발견: {src[:100]}...")
                            break
            else:
                img = soup.select_one(selector)
                if img and img.get('src'):
                    src = img.get('src')
                    if src and (src.startswith('http') or src.startswith('/')):
                        if not src.startswith('http'):
                            from urllib.parse import urljoin
                            src = urljoin(url, src)
                        if any(ext in src.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp', '.gif']):
                            image_url = src
                            logger.info(f"이미지 발견: {src[:100]}...")
                            break
        
        return content[:1500] if content else "", image_url
        
    except Exception as e:
        logger.error(f"기사 내용 추출 실패 ({url[:50]}...): {e}")
        return "", ""

def get_optimized_space_news():
    """최적화된 우주 뉴스 수집"""
    # 구글 뉴스 우선 시도
    articles = crawl_google_news_optimized()
    
    if articles:
        logger.info(f"구글 뉴스에서 {len(articles)}개 최신 뉴스 수집 성공")
        return articles
    
    # 실패시 빈 리스트 반환
    logger.warning("모든 뉴스 소스 실패 - 실제 데이터 없음")
    return []