import logging
from datetime import datetime
from crawler.all_observatory_crawler import crawl_all_korea_observatories

logger = logging.getLogger(__name__)

async def crawl_observatory_only():
    """천문대 견학 일정만 크롤링"""
    logger.info(f"천문대 견학 일정 크롤링 시작: {datetime.now()}")
    
    # 전국 천문대 크롤링만 실행
    korea_observatories_result = await crawl_all_korea_observatories()
    
    logger.info(f"천문대 견학 일정 크롤링 완료: 총 {korea_observatories_result['total_events']}개 중 {korea_observatories_result['success']}개 전송 성공")
    logger.info(f"포함된 천문대: {korea_observatories_result['total_observatories']}개소")
    
    return korea_observatories_result