#!/usr/bin/env python3
"""
DB 기반 중복 게시글 체크 시스템
"""
import logging
import requests
from typing import List, Dict
from config import SPRING_SERVER_URL, API_KEY

logger = logging.getLogger(__name__)

def check_existing_posts(titles: List[str]) -> List[str]:
    """스프링 서버 DB에서 기존 게시글 제목 확인"""
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': API_KEY
        }
        
        # 최근 7일간 뉴스 게시글 제목 조회
        response = requests.get(
            f"{SPRING_SERVER_URL}/api/admin/crawler/check-duplicates",
            headers=headers,
            params={'days': 7, 'category': 'NEWS'},
            timeout=10
        )
        
        if response.status_code == 200:
            existing_titles = response.json().get('titles', [])
            logger.info(f"DB에서 {len(existing_titles)}개 기존 제목 조회")
            return existing_titles
        else:
            logger.warning(f"DB 조회 실패: {response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"DB 중복 체크 실패: {e}")
        return []

def is_duplicate_title(new_title: str, existing_titles: List[str]) -> bool:
    """제목 중복 여부 확인 (유사도 포함)"""
    try:
        # 정확한 일치 확인
        if new_title in existing_titles:
            return True
        
        # 유사도 확인 (85% 이상 유사하면 중복으로 판단) - 조건 완화
        for existing_title in existing_titles:
            similarity = calculate_similarity(new_title, existing_title)
            if similarity > 0.85:
                logger.info(f"유사 제목 발견: '{new_title}' vs '{existing_title}' (유사도: {similarity:.2f})")
                return True
        
        # 핵심 키워드 기반 중복 체크
        new_keywords = extract_key_words(new_title)
        for existing_title in existing_titles:
            existing_keywords = extract_key_words(existing_title)
            common_keywords = new_keywords & existing_keywords
            if len(common_keywords) >= 2 and len(common_keywords) / len(new_keywords) > 0.7:
                logger.info(f"키워드 기반 중복: '{new_title}' (공통: {common_keywords})")
                return True
        
        return False
        
    except Exception as e:
        logger.error(f"중복 체크 오류: {e}")
        return False

def extract_key_words(title: str) -> set:
    """제목에서 핵심 키워드 추출"""
    # 의미있는 단어들만 추출
    import re
    words = re.findall(r'[가-힣A-Za-z0-9]+', title)
    # 짧은 단어나 일반적인 단어 제외
    meaningful_words = set()
    for word in words:
        if (len(word) >= 2 and 
            word not in ['우주', '뉴스', '최신', '관련', '소식', '발표']):
            meaningful_words.add(word)
    return meaningful_words

def calculate_similarity(title1: str, title2: str) -> float:
    """두 제목 간 유사도 계산 (간단한 방식)"""
    try:
        # 공통 단어 비율로 유사도 계산
        words1 = set(title1.replace(' ', ''))
        words2 = set(title2.replace(' ', ''))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
        
    except Exception as e:
        logger.error(f"유사도 계산 오류: {e}")
        return 0.0

def filter_duplicate_articles(articles: List[Dict]) -> List[Dict]:
    """중복 기사 필터링 (DB + 스마트 로컬 캐시)"""
    try:
        if not articles:
            return []
        
        # 새로운 기사 제목들 추출
        new_titles = [article.get('title', '') for article in articles]
        
        # 1차: DB에서 기존 제목들 조회
        existing_titles = check_existing_posts(new_titles)
        
        # 2차: 스마트 로컬 캐시 체크 (30분 이내만 중복 방지)
        from utils.local_cache import get_smart_cached_titles, save_cached_titles
        recent_cached_titles = get_smart_cached_titles(minutes=30)  # 30분 이내만 중복 체크
        all_existing_titles = list(set(existing_titles) | recent_cached_titles)
        
        logger.info(f"중복 체크: DB {len(existing_titles)}개 + 캐시 {len(recent_cached_titles)}개 = 총 {len(all_existing_titles)}개")
        
        # 중복되지 않은 기사만 필터링
        filtered_articles = []
        new_article_titles = []
        
        for article in articles:
            title = article.get('title', '')
            if not is_duplicate_title(title, all_existing_titles):
                filtered_articles.append(article)
                new_article_titles.append(title)
                logger.info(f"새로운 기사: {title[:50]}...")
            else:
                logger.info(f"중복 기사 제외: {title[:50]}...")
        
        # 새로운 제목들을 로컬 캐시에 저장
        if new_article_titles:
            save_cached_titles(new_article_titles)
        
        logger.info(f"중복 필터링 결과: {len(articles)}개 → {len(filtered_articles)}개")
        return filtered_articles
        
    except Exception as e:
        logger.error(f"중복 필터링 실패: {e}")
        return articles  # 실패 시 원본 반환

def create_title_hash(title: str) -> str:
    """제목의 해시값 생성 (중복 체크용)"""
    import hashlib
    return hashlib.md5(title.encode('utf-8')).hexdigest()[:16]