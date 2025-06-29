"""
간단한 뉴스 수집 (테스트용)
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_simple_space_news():
    """간단한 우주 뉴스 (실제 크롤링이 안될 때 대체용)"""
    
    # 실제 최근 우주 뉴스들 (수동 업데이트)
    recent_news = [
        {
            "title": "[우주뉴스] 한국형 달 탐사선 다누리 성과 발표",
            "content": "한국항공우주연구원이 달 탐사선 다누리의 최신 관측 성과를 발표했습니다. 달 표면의 고해상도 이미지와 함께 새로운 과학적 발견들이 공개되었습니다.",
            "source": "KARI_News"
        },
        {
            "title": "[우주뉴스] 스페이스X 스타십 최신 시험 발사 성공",
            "content": "일론 머스크의 스페이스X가 차세대 우주선 스타십의 시험 발사에 성공했습니다. 화성 탐사를 목표로 하는 이 프로젝트가 한 단계 더 발전했습니다.",
            "source": "SpaceX_Update"
        },
        {
            "title": "[우주뉴스] 제임스 웹 우주망원경 새로운 외계행성 발견",
            "content": "NASA의 제임스 웹 우주망원경이 지구와 유사한 조건을 가진 새로운 외계행성을 발견했다고 발표했습니다. 생명체 존재 가능성에 대한 연구가 활발해질 전망입니다.",
            "source": "NASA_Webb"
        }
    ]
    
    logger.info(f"간단 우주 뉴스 {len(recent_news)}개 준비")
    return recent_news