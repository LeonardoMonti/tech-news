import requests
import time
from parsel import Selector


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
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
