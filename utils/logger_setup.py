import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger():
    """로그 시스템 설정"""
    
    # 로그 디렉토리 생성
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 기존 핸들러 제거
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 파일 핸들러 (회전 로그)
    file_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "crawler.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    # 에러 전용 파일 핸들러
    error_handler = RotatingFileHandler(
        filename=os.path.join(log_dir, "error.log"),
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_crawling_result(crawler_type: str, result: dict):
    """크롤링 결과 로그 기록"""
    logger = logging.getLogger(__name__)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if crawler_type == "news":
        logger.info(f"📰 [{timestamp}] 뉴스 크롤링 완료 - 총 {result['total']}개 중 {result['success']}개 성공")
        logger.info(f"📰 [{timestamp}] 뉴스 소스: {', '.join(result['sources'])}")
    elif crawler_type == "observatory":
        logger.info(f"🏛️ [{timestamp}] 천문대 일정 크롤링 완료 - 총 {result['total_events']}개 중 {result['success']}개 성공")
        logger.info(f"🏛️ [{timestamp}] 천문대: {', '.join(result['observatories'])}")
    
    # 실패가 있으면 에러 로그에도 기록
    if result.get('success', 0) < result.get('total', 0) or result.get('success', 0) < result.get('total_events', 0):
        failed_count = result.get('total', result.get('total_events', 0)) - result.get('success', 0)
        logger.error(f"❌ [{timestamp}] {crawler_type} 크롤링 중 {failed_count}개 실패")

def log_duplicate_skip(source: str, title: str, reason: str):
    """중복 처리 로깅"""
    logger = logging.getLogger('duplicate')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"🔄 [{timestamp}] [{source}] 중복 처리: {title[:50]}... - {reason}")

def log_retry_failure(source: str, title: str, attempts: int):
    """재시도 실패 로깅"""
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.error(f"❌ [{timestamp}] [{source}] 최종 실패 ({attempts}회 시도): {title[:50]}...")

def log_crawling_error(source: str, error: str, url: str = None):
    """크롤링 에러 로깅"""
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error_msg = f"🚨 [{timestamp}] [{source}] 크롤링 실패: {error}"
    if url:
        error_msg += f" - URL: {url}"
    logger.error(error_msg)