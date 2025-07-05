#!/usr/bin/env python3
"""
뉴스 AI 요약 및 품질 평가 시스템
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def evaluate_news_article(title: str, content: str, link: str) -> Dict:
    """뉴스 기사 평가 및 요약"""
    try:
        # 우주 관련 키워드 체크
        space_keywords = [
            '우주', '천문', '별', '달', '행성', '로켓', '위성', '화성', '태양', '은하',
            '망원경', '탐사', '항공', 'NASA', '우주정거장', '혜성', '소행성', '블랙홀',
            '제임스웹', '누리호', '스페이스X', '아르테미스', '화성탐사', '달착륙'
        ]
        
        # 제외할 키워드 (연예/아이돌 및 투자/금융 뉴스 포함)
        exclude_keywords = [
            '코로나', '백신', '의료', '병원', '치료', '약물', '건강',
            '정치', '경제', '부동산', '주식', '금융', '선거', 'ETF', '투자', '수익률', '펀드', '방산',
            '우주소녀', '팬미팅', '콘서트', '아이돌', '가수', '연예인', '음악', '앨범'
        ]
        
        title_lower = title.lower()
        content_lower = content.lower()
        
        # 제외 키워드 체크
        if any(keyword in title_lower or keyword in content_lower for keyword in exclude_keywords):
            return {
                "evaluation": "REJECT",
                "summary": "",
                "keywords": [],
                "reason": "일반 과학/사회 뉴스"
            }
        
        # 우주 키워드 체크
        space_score = sum(1 for keyword in space_keywords 
                         if keyword in title_lower or keyword in content_lower)
        
        if space_score < 1:
            return {
                "evaluation": "REJECT", 
                "summary": "",
                "keywords": [],
                "reason": "우주 관련성 부족"
            }
        
        # 키워드 추출
        found_keywords = [keyword for keyword in space_keywords 
                         if keyword in title_lower or keyword in content_lower][:3]
        
        # 더 구체적이고 흥미로운 요약 생성
        title_lower = title.lower()
        
        if '우주의 끝' in title:
            summary = "우주의 경계와 크기에 대한 과학적 탐구입니다. 우주론과 물리학의 기본 질문을 다룹니다."
        elif '한양대' in title and 'ssp' in title_lower:
            summary = "한양대 ERICA가 국내 최초로 국제우주대학 우주연구 프로그램을 개최합니다. 한국 우주교육의 새로운 이정표입니다."
        elif '블랙홀' in title or '중력파' in title:
            summary = "블랙홀이나 중력파 관련 최신 연구 결과입니다. 우주의 기본 원리를 이해하는 데 도움이 됩니다."
        elif '외계인' in title or '생명체' in title:
            summary = "외계 생명체 탐사나 관련 연구 소식입니다. 인류의 우주에서의 위치를 새롭게 생각하게 합니다."
        elif '화성' in title and ('탐사' in title or '착륙' in title):
            summary = "화성 탐사 미션의 새로운 소식입니다. 인류의 화성 정착 꿈에 한 걸음 더 가까워졌습니다."
        elif '달' in title and ('기지' in title or '정착' in title):
            summary = "달 기지 건설이나 달 정착 계획 관련 소식입니다. 인류의 우주 시대가 본격화되고 있습니다."
        elif '제임스웹' in title or 'jwst' in title_lower:
            summary = "제임스웹 우주망원경의 새로운 발견입니다. 우주의 초기 모습을 더 선명하게 보여주고 있습니다."
        elif '누리호' in title or '한국형' in title:
            summary = "한국의 누리호 로켓 관련 소식입니다. 한국이 우주 강국으로 도약하고 있습니다."
        elif '발사' in title or '성공' in title:
            summary = "우주 발사체나 인공위성 발사 성공 소식입니다. 우주 기술의 눈부신 발전을 보여줍니다."
        else:
            # 제목에서 핵심 내용 추출
            if '?' in title:
                summary = f"우주에 대한 흥미로운 질문을 다룹니다. 과학적 호기심을 자극하는 내용입니다."
            else:
                key_topic = title.split(',')[0].split('-')[0].strip()[:40]
                summary = f"{key_topic}에 대한 우주 과학 소식입니다. 우주의 신비를 풀어가는 여정입니다."
        
        return {
            "evaluation": "ACCEPT",
            "summary": summary,
            "keywords": found_keywords,
            "space_score": space_score
        }
        
    except Exception as e:
        logger.error(f"뉴스 평가 실패: {e}")
        return {
            "evaluation": "ACCEPT",
            "summary": f"{title}. 우주 관련 최신 소식입니다.",
            "keywords": ["우주", "뉴스", "과학"],
            "reason": "백업 평가"
        }