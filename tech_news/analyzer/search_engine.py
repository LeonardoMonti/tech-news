from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    result = []
    search = search_news(
        {
            "title": {
                "$regex": f"{title.lower()}",
            }
        }
    )

    for item in search:
        result.append((item["title"], item["url"]))

    return result


# Requisito 7
def search_by_date(date):
    try:
        result = []
        format_date = datetime.strptime(date, "%Y-%m-%d")
        if type(format_date) is not datetime:
            raise ValueError
        search = search_news(
            {
                "timestamp": "/".join(reversed(date.split("-"))),
            }
        )
        for item in search:
            result.append((item["title"], item["url"]))

        return result
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    result = []
    search = search_news({"tags": f"{tag.casefold().capitalize()}"})

    for news in search:
        result.append((news["title"], news["url"]))

    return result


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
