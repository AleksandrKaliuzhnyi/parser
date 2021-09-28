import json
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}


def get_first_news():
    url = "https://www.securitylab.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    article_cards = soup.find_all("a", class_="article-card")

    news_dict = {}
    for article in article_cards:
        article_title = article.find("h2", class_="article-card-title").text.strip()
        article_desc = article.find("p").text.strip()
        article_url = f"https://www.securitylab.ru{article.get('href')}"

        article_date_time = article.find("time").get("datetime")
        date_time_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_time_iso, "%Y-%m-%d %H-%M-%S")
        article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H-%M-%S").timetuple())

        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        # print(f"{article_title} | {article_url} | {article_date_timestamp}")

        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }

    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_news_update():
    with open("news.json", encoding="utf-8") as file:
        news_dict = json.load(file)

    url = "https://www.securitylab.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    article_cards = soup.find_all("a", class_="article-card")

    fresh_news = {}
    for article in article_cards:
        article_url = f"https://www.securitylab.ru{article.get('href')}"
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()

            article_date_time = article.find("time").get("datetime")
            date_time_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_time_iso, "%Y-%m-%d %H-%M-%S")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H-%M-%S").timetuple())

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_first_news()
    check_news_update()


if __name__ == "__main__":
    main()
