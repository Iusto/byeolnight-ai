# FastAPI 설정 파일
import os

# 스프링 서버 설정
SPRING_SERVER_URL = "http://localhost:8080"
API_KEY = "byeolnight-crawler-news"  # 뉴스용 API 키
EVENT_API_KEY = "byeolnight-crawler-exhibitions"  # 전시회용 API 키

# 크롤링 설정
MAX_ARTICLES_PER_SOURCE = 3
REQUEST_TIMEOUT = 30

# 중복 처리 설정
MAX_RETRY_COUNT = 5  # 최대 재시도 횟수
DUPLICATE_CHECK_ENABLED = True  # 중복 체크 활성화

# 작성자 ID 설정
NEWS_AUTHOR_ID = "newsbot"  # 뉴스봇 ID
EXHIBITION_AUTHOR_ID = "exhibitionbot"  # 전시회봇 ID

# 로깅 설정
LOG_LEVEL = "INFO"
LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5