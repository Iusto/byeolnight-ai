import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime
import logging
import sys
import os
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 상위 디렉토리의 config 모듈 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SPRING_SERVER_URL, API_KEY, REQUEST_TIMEOUT
from crawler.korean_news_crawler import crawl_all_korean_content

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 한국형 통합 크롤링 함수로 교체
async def crawl_all_content():
    """한국 뉴스와 천문대 일정 모두 크롤링"""
    return await crawl_all_korean_content()

# 하위 호환성을 위한 별칭
async def crawl_all_news():
    """뉴스 크롤링 (한국형 통합 크롤링으로 리다이렉트)"""
    return await crawl_all_korean_content()