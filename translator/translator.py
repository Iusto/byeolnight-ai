import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def translate_text(text: str, target_lang: str = 'ko') -> Optional[str]:
    """
    Google Translate API를 사용하여 텍스트 번역
    무료 API 사용 (제한적)
    """
    if not text or not text.strip():
        return text
    
    try:
        # Google Translate 무료 API 사용
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'auto',  # 자동 언어 감지
            'tl': target_lang,
            'dt': 't',
            'q': text
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # 번역된 텍스트 추출
            translated_text = ''.join([item[0] for item in result[0] if item[0]])
            logger.info(f"번역 성공: {text[:50]}... -> {translated_text[:50]}...")
            return translated_text
        else:
            logger.error(f"번역 API 오류: {response.status_code}")
            return text
            
    except Exception as e:
        logger.error(f"번역 실패: {e}")
        return text

def is_english_text(text: str) -> bool:
    """텍스트가 주로 영어인지 확인"""
    if not text:
        return False
    
    # 영어 문자 비율 계산
    english_chars = sum(1 for c in text if c.isalpha() and ord(c) < 128)
    total_chars = sum(1 for c in text if c.isalpha())
    
    if total_chars == 0:
        return False
    
    english_ratio = english_chars / total_chars
    return english_ratio > 0.7  # 70% 이상이 영어면 영어 텍스트로 판단

def translate_news_content(title: str, content: str) -> tuple[str, str]:
    """뉴스 제목과 내용을 번역 (필요한 경우에만)"""
    translated_title = title
    translated_content = content
    
    # 제목 번역 (영어인 경우에만)
    if is_english_text(title):
        translated_title = translate_text(title) or title
    
    # 내용 번역 (영어인 경우에만)
    if is_english_text(content):
        translated_content = translate_text(content) or content
    
    return translated_title, translated_content