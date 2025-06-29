from fastapi import FastAPI
from crawler.news_crawler import crawl_sciencetimes_news

app = FastAPI()

@app.get("/news")
def get_news(count: int = 2):
    return crawl_sciencetimes_news(count)
