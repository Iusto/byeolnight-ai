import requests
from bs4 import BeautifulSoup

def crawl_sciencetimes_news(count=2):
    url = "https://www.sciencetimes.co.kr/news/category/%ec%9a%b0%ec%a3%bc%eb%b3%91%ea%b3%84"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")

    articles = []
    for item in soup.select("ul.article-list li")[:count]:
        title_tag = item.select_one("h4 a")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = title_tag["href"]
        summary_tag = item.select_one("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""

        articles.append({
            "title": title,
            "summary": summary,
            "url": link
        })
    return articles
