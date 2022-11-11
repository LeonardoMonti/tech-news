import requests
import time
from parsel import Selector
import re
from tech_news.database import create_news


# https://stackoverflow.com/questions/26825729/extract-number-from-string-in-python
# Requisito 1
def fetch(url: str):
    time.sleep(1)
    header = {"user-agent": "Fake user-agent"}
    try:
        html = requests.get(url, headers=header, timeout=1)
        html.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    return html.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    novidades = []
    articles = selector.css("div.archive-main > article.entry-preview")

    for article in articles:
        novidades.append(
            article.css(
                """
                div.post-inner > header.entry-header >
                h2.entry-title > a ::attr(href)
                """
            ).get()
        )

    return novidades


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    next_link = selector.css(
        """
        div.nav-links > a.next ::attr(href)
        """
    ).get()

    return next_link


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(html_content)

    comments_count = selector.css(
        "div.post-comments h5.title-block ::text"
    ).get()
    if comments_count is None:
        comments_count = 0
    else:
        comments_count = int(re.search(r"\d+", comments_count).group())

    url = selector.css('link[rel="canonical"]::attr(href)').get()
    title = selector.css("div.entry-header-inner h1.entry-title ::text").get()
    timestamp = selector.css("ul.post-meta > li.meta-date ::text").get()
    writer = selector.css("span.author a.url ::text").get()

    summarys = selector.css(
        "div.entry-content > p:nth-of-type(1) *::text"
    ).getall()

    tags = selector.css(
        "section.post-tags ul li:not(:first-child) ::text"
    ).getall()

    category = selector.css(
        "div.meta-category a.category-style span.label ::text"
    ).get()

    news = {
        "url": url,
        "title": title.strip(),
        "timestamp": timestamp,
        "writer": writer,
        "comments_count": comments_count,
        "summary": "".join(summarys).strip(),
        "tags": tags,
        "category": category,
    }
    return news


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com"
    next_url = "/"
    news = []

    content = fetch(url)
    if content is not None:
        while next_url:
            url_news = scrape_novidades(content)
            for url_new in url_news:
                content_new = fetch(url_new)
                news.append(scrape_noticia(content_new))
                if len(news) >= amount:
                    create_news(news)
                    return news
            next_url = scrape_next_page_link(content)
            content = fetch(next_url)
    create_news(news)
    return news
