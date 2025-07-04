from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from crawler.news_only_crawler import crawl_news_only
from crawler.exhibition_crawler import crawl_space_exhibitions
import uvicorn
import logging
import requests
from config import SPRING_SERVER_URL
from utils.logger_setup import setup_logger, log_crawling_result, log_crawling_error

# 로그 시스템 설정
setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(title="AI 우주 정보 크롤러", description="우주 뉴스와 전시회 정보 크롤링 시스템")
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 스케줄러 시작"""
    # 우주 뉴스 크롤링: 하루 1회 (오전 8시) - 3개 뉴스 보장
    scheduler.add_job(
        crawl_news_only,
        CronTrigger(hour=8, minute=0),
        id="daily_news",
        name="오전 8시 우주 뉴스 크롤링 (3개 보장)"
    )
    
    # 우주 전시회 크롤링: 하루 1회 (오전 10시) - 뉴스와 시간 분리
    scheduler.add_job(
        crawl_space_exhibitions,
        CronTrigger(hour=10, minute=0),
        id="daily_exhibitions",
        name="오전 10시 우주 전시회 크롤링"
    )
    
    scheduler.start()
    logger.info("우주 정보 크롤링 스케줄러 시작됨")
    logger.info("  - 우주 뉴스 (3개 보장): 매일 08:00")
    logger.info("  - 우주 전시회: 매일 10:00")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 스케줄러 종료"""
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {
        "message": "AI 우주 정보 크롤러 서버 실행 중", 
        "news_schedule": ["08:00 (3개 보장)"],
        "exhibition_schedule": ["10:00"],
        "features": ["우주 뉴스 크롤링 (NEWS) - 3개 보장", "우주 전시회 크롤링 (EVENT)"],
        "news_sources": ["구글뉴스RSS", "최신뉴스필터링", "AI요약시스템"]
    }

@app.post("/crawl-news")
async def manual_news_crawl():
    """수동 뉴스 크롤링 실행"""
    try:
        result = await crawl_news_only()
        log_crawling_result("news", result)
        return {"message": "뉴스 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"수동 뉴스 크롤링 오류: {e}")
        raise HTTPException(status_code=500, detail=f"뉴스 크롤링 오류: {str(e)}")

@app.post("/crawl-exhibitions")
async def manual_exhibition_crawl():
    """수동 우주 전시회 크롤링 실행"""
    try:
        result = await crawl_space_exhibitions()
        log_crawling_result("exhibitions", result)
        return {"message": "우주 전시회 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"수동 전시회 크롤링 오류: {e}")
        raise HTTPException(status_code=500, detail=f"전시회 크롤링 오류: {str(e)}")

@app.get("/status")
def get_status():
    """스케줄러 상태 확인"""
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": str(job.next_run_time) if job.next_run_time else None
        })
    return {"scheduler_running": scheduler.running, "jobs": jobs}

@app.get("/health")
def health_check():
    """헬스체크 및 스프링 서버 연결 확인"""
    try:
        response = requests.get(f"{SPRING_SERVER_URL}/api/admin/crawler/status", timeout=5)
        spring_status = "connected" if response.status_code == 200 else "disconnected"
    except:
        spring_status = "disconnected"
    
    return {
        "fastapi_status": "running",
        "spring_server_status": spring_status,
        "scheduler_running": scheduler.running if 'scheduler' in globals() else False
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)