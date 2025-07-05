#!/usr/bin/env python3
"""
로컬 캐시 기반 중복 방지 시스템 (DB 백업용)
"""
import json
import os
import logging
from datetime import datetime, timedelta
from typing import List, Set

logger = logging.getLogger(__name__)

CACHE_FILE = "data/news_cache.json"

def ensure_data_dir():
    """data 디렉토리 생성"""
    os.makedirs("data", exist_ok=True)

def load_cached_titles() -> Set[str]:
    """캐시된 제목들 로드 (7일 이내)"""
    try:
        ensure_data_dir()
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # 7일 이내 제목만 유지
            cutoff_date = datetime.now() - timedelta(days=7)
            valid_titles = set()
            
            for entry in cache_data:
                entry_date = datetime.fromisoformat(entry['date'])
                if entry_date >= cutoff_date:
                    valid_titles.add(entry['title'])
            
            logger.info(f"로컬 캐시에서 {len(valid_titles)}개 제목 로드")
            return valid_titles
        else:
            return set()
    except Exception as e:
        logger.error(f"캐시 로드 실패: {e}")
        return set()

def load_cached_titles_recent(hours: int = 1) -> Set[str]:
    """최근 N시간 이내 캐시된 제목들 로드"""
    try:
        ensure_data_dir()
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # N시간 이내 제목만 유지
            cutoff_date = datetime.now() - timedelta(hours=hours)
            recent_titles = set()
            
            for entry in cache_data:
                entry_date = datetime.fromisoformat(entry['date'])
                if entry_date >= cutoff_date:
                    recent_titles.add(entry['title'])
            
            logger.info(f"로컬 캐시에서 {hours}시간 이내 {len(recent_titles)}개 제목 로드")
            return recent_titles
        else:
            return set()
    except Exception as e:
        logger.error(f"최근 캐시 로드 실패: {e}")
        return set()

def save_cached_titles(titles: List[str]):
    """새로운 제목들을 캐시에 저장"""
    try:
        ensure_data_dir()
        
        # 기존 캐시 로드
        existing_cache = []
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                existing_cache = json.load(f)
        
        # 새로운 제목들 추가
        current_time = datetime.now().isoformat()
        for title in titles:
            existing_cache.append({
                'title': title,
                'date': current_time
            })
        
        # 7일 이내 데이터만 유지
        cutoff_date = datetime.now() - timedelta(days=7)
        filtered_cache = []
        for entry in existing_cache:
            entry_date = datetime.fromisoformat(entry['date'])
            if entry_date >= cutoff_date:
                filtered_cache.append(entry)
        
        # 캐시 저장
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(filtered_cache, f, ensure_ascii=False, indent=2)
        
        logger.info(f"로컬 캐시에 {len(titles)}개 제목 저장")
        
    except Exception as e:
        logger.error(f"캐시 저장 실패: {e}")

def get_smart_cached_titles(minutes: int = 30) -> Set[str]:
    """스마트 캐시: N분 이내만 중복 체크"""
    try:
        ensure_data_dir()
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # N분 이내 제목만 유지
            cutoff_date = datetime.now() - timedelta(minutes=minutes)
            recent_titles = set()
            
            for entry in cache_data:
                entry_date = datetime.fromisoformat(entry['date'])
                if entry_date >= cutoff_date:
                    recent_titles.add(entry['title'])
            
            logger.info(f"로컬 캐시에서 {minutes}분 이내 {len(recent_titles)}개 제목 로드")
            return recent_titles
        else:
            logger.info(f"캐시 파일 없음 - 0개 제목 로드")
            return set()
    except Exception as e:
        logger.error(f"스마트 캐시 로드 실패: {e}")
        return set()

def is_duplicate_local(title: str, hours: int = 24) -> bool:
    """로컬 캐시 기반 중복 체크"""
    try:
        if hours <= 24:
            cached_titles = load_cached_titles_recent(hours)
        else:
            cached_titles = load_cached_titles()
        return title in cached_titles
    except Exception as e:
        logger.error(f"로컬 중복 체크 실패: {e}")
        return False