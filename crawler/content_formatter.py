import re
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def clean_and_format_content(content: str) -> str:
    """기사 내용을 정리하고 포맷팅"""
    if not content:
        return "기사 내용을 가져올 수 없습니다."
    
    # 불필요한 텍스트 제거
    unwanted_patterns = [
        r'쿠키.*?수락.*?',
        r'다운로드.*?MB.*?',
        r'소스.*?MB.*?',
        r'좋아요.*?조회.*?',
        r'ID.*?\d+.*?',
        r'라이센스.*?표준.*?',
        r'YouTube.*?컨트롤.*?',
        r'음악 클립.*?',
        r'포함 코드.*?',
        r'캡션.*?자막.*?',
        r'\d{2}/\d{2}/\d{4}.*?\d+.*?조회',
        r'00:\d{2}:\d{2}',
        r'MP4.*?\[.*?MB\]',
    ]
    
    cleaned_content = content
    for pattern in unwanted_patterns:
        cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.IGNORECASE)
    
    # 연속된 공백과 줄바꿈 정리
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
    cleaned_content = re.sub(r'\n\s*\n', '\n\n', cleaned_content)
    
    # 문장 단위로 정리
    sentences = [s.strip() for s in cleaned_content.split('.') if s.strip() and len(s.strip()) > 10]
    
    # 의미있는 문장들만 선별 (최대 5문장)
    meaningful_sentences = []
    for sentence in sentences[:8]:
        if len(sentence) > 20 and not any(word in sentence.lower() for word in 
                                        ['쿠키', 'youtube', '다운로드', '라이센스', '클립']):
            meaningful_sentences.append(sentence.strip() + '.')
    
    return ' '.join(meaningful_sentences[:5]) if meaningful_sentences else content[:500]

def extract_image_url(soup, base_url: str) -> Optional[str]:
    """기사에서 대표 이미지 URL 추출"""
    try:
        # 일반적인 이미지 선택자들
        img_selectors = [
            'meta[property="og:image"]',
            'meta[name="twitter:image"]',
            '.article-image img',
            '.post-image img',
            '.featured-image img',
            'article img',
            '.content img'
        ]
        
        for selector in img_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                img_url = img_elem.get('content') or img_elem.get('src')
                if img_url:
                    # 상대 URL을 절대 URL로 변환
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = base_url + img_url
                    elif not img_url.startswith('http'):
                        img_url = base_url + '/' + img_url
                    
                    return img_url
        
        return None
    except Exception as e:
        logger.error(f"이미지 추출 실패: {e}")
        return None

def format_news_article(title: str, content: str, source: str, url: str, image_url: Optional[str] = None) -> Tuple[str, str]:
    """뉴스 기사를 보기 좋게 포맷팅"""
    
    # 제목 정리
    clean_title = title.replace('[', '').replace(']', '').strip()
    if not clean_title.startswith('['):
        clean_title = f"[{source}] {clean_title}"
    
    # 내용 정리 및 포맷팅
    clean_content = clean_and_format_content(content)
    
    # 기사 본문 구성
    formatted_content = f"""📰 **{source} 뉴스**

{clean_content}

---
🔗 **원문 보기**: {url}
📅 **발행**: {source}
🏷️ **카테고리**: 우주/천문학"""

    # 이미지가 있으면 추가
    if image_url:
        formatted_content = f"""📰 **{source} 뉴스**

🖼️ ![뉴스 이미지]({image_url})

{clean_content}

---
🔗 **원문 보기**: {url}
📅 **발행**: {source}
🏷️ **카테고리**: 우주/천문학"""
    
    return clean_title, formatted_content

def create_summary(content: str) -> str:
    """기사 내용에서 요약 생성"""
    sentences = [s.strip() for s in content.split('.') if s.strip() and len(s.strip()) > 20]
    
    # 첫 2-3문장으로 요약 생성
    summary_sentences = sentences[:3]
    summary = '. '.join(summary_sentences)
    
    if len(summary) > 200:
        summary = summary[:197] + "..."
    
    return summary + "." if summary and not summary.endswith('.') else summary