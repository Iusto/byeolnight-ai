import requests
import logging
from typing import Optional
import time
import random

logger = logging.getLogger(__name__)

def translate_with_deepl_free(text: str) -> Optional[str]:
    """DeepL 무료 번역 (더 자연스러운 번역)"""
    try:
        # DeepL 무료 API 사용 (일일 제한 있음)
        url = "https://api-free.deepl.com/v2/translate"
        
        # 실제로는 DeepL API 키가 필요하지만, 
        # 여기서는 다른 무료 서비스 사용
        return None
        
    except Exception as e:
        logger.error(f"DeepL 번역 실패: {e}")
        return None

def translate_with_papago(text: str) -> Optional[str]:
    """네이버 파파고 번역 (무료, 한국어 특화)"""
    try:
        # 파파고는 API 키가 필요하므로 생략
        return None
    except Exception as e:
        logger.error(f"파파고 번역 실패: {e}")
        return None

def enhanced_google_translate(text: str) -> str:
    """개선된 Google Translate (무료)"""
    from translator.translator import translate_text
    
    # 긴 텍스트를 문장 단위로 나누어 번역 (품질 향상)
    sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
    
    translated_sentences = []
    for sentence in sentences:
        if len(sentence) > 10:  # 의미있는 문장만
            translated = translate_text(sentence)
            if translated:
                translated_sentences.append(translated)
            time.sleep(0.1)  # API 제한 방지
    
    return ' '.join(translated_sentences)

def post_process_translation(text: str) -> str:
    """번역 후처리로 품질 개선"""
    # 일반적인 번역 오류 수정
    corrections = {
        '국제 우주 정거장': '국제우주정거장',
        '나사': 'NASA',
        '이사': 'ESA',
        '유럽 우주국': '유럽우주국',
        '우주 비행사': '우주비행사',
        '인공 위성': '인공위성',
        '태양 전지판': '태양전지판',
        '우주선': '우주선',
        '로켓': '로켓',
        '발사': '발사',
        '궤도': '궤도',
        '달': '달',
        '화성': '화성',
        '목성': '목성',
        '토성': '토성',
        '천왕성': '천왕성',
        '해왕성': '해왕성',
        '명왕성': '명왕성',
        '태양계': '태양계',
        '은하': '은하',
        '블랙홀': '블랙홀',
        '중성자별': '중성자별',
        '초신성': '초신성'
    }
    
    result = text
    for wrong, correct in corrections.items():
        result = result.replace(wrong, correct)
    
    return result

def smart_free_translate(title: str, content: str) -> tuple[str, str]:
    """무료 서비스를 활용한 스마트 번역"""
    from translator.translator import is_english_text
    
    translated_title = title
    translated_content = content
    
    # 제목 번역
    if is_english_text(title):
        translated_title = enhanced_google_translate(title)
        translated_title = post_process_translation(translated_title)
    
    # 내용 번역
    if is_english_text(content):
        translated_content = enhanced_google_translate(content)
        translated_content = post_process_translation(translated_content)
    
    return translated_title, translated_content