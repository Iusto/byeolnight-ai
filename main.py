from fastapi import FastAPI, HTTPException
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from crawler.news_only_crawler import crawl_news_only
from crawler.observatory_schedule_crawler import crawl_observatory_schedules
import uvicorn
import logging
import requests
from config import SPRING_SERVER_URL
from utils.logger_setup import setup_logger, log_crawling_result, log_crawling_error

# 로그 시스템 설정
setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(title="AI 분리형 크롤러", description="뉴스와 천문대 일정 분리 크롤링 시스템")
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 스케줄러 시작"""
    # 뉴스 크롤링: 하루 2회 (오전 6시, 오후 12시)
    scheduler.add_job(
        crawl_news_only,
        CronTrigger(hour=6, minute=0),
        id="morning_news",
        name="오전 6시 우주 뉴스 크롤링"
    )
    scheduler.add_job(
        crawl_news_only,
        CronTrigger(hour=12, minute=0),
        id="noon_news",
        name="오후 12시 우주 뉴스 크롤링"
    )
    
    # 천문대 일정 크롤링: 하루 1회 (오전 7시)
    scheduler.add_job(
        crawl_observatory_schedules,
        CronTrigger(hour=7, minute=0),
        id="morning_observatory",
        name="오전 7시 천문대 일정 크롤링"
    )
    
    scheduler.start()
    logger.info("분리형 크롤링 스케줄러 시작됨")
    logger.info("  - 뉴스: 매일 06:00, 12:00")
    logger.info("  - 천문대: 매일 07:00")

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 스케줄러 종료"""
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {
        "message": "AI 분리형 크롤러 서버 실행 중", 
        "news_schedule": ["06:00", "12:00"],
        "observatory_schedule": ["07:00"],
        "features": ["우주 뉴스 크롤링 (NEWS)", "천문대 일정 크롤링 (EVENT)"]
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

@app.post("/crawl-observatory")
async def manual_observatory_crawl():
    """수동 천문대 일정 크롤링 실행"""
    try:
        result = await crawl_observatory_schedules()
        log_crawling_result("observatory", result)
        return {"message": "천문대 일정 크롤링 완료", "result": result}
    except Exception as e:
        logger.error(f"수동 천문대 크롤링 오류: {e}")
        raise HTTPException(status_code=500, detail=f"천문대 크롤링 오류: {str(e)}")

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