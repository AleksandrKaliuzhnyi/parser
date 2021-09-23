import requests
from bs4 import BeautifulSoup
import lxml
import os
import time


def get_all_pages():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    # r = requests.get(url="https://shop.casio.ru/catalog/filter/gender-is-male/apply/", headers=headers)
    #
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open ("data/page_1.html", "w", encoding="utf-8") as file:
    #     file.write(r.text)

    with open("data/page_1.html", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    # -2 because the last element in "a" is arrow
    pages_count = int(soup.find("div", class_="bx-pagination-container").find_all("a")[-2].text)

    for i in range(1, pages_count + 1):
        url = f"https://shop.casio.ru/catalog/filter/gender-is-male/apply/?PAGEN_1={i}"
        print(url)

        r = requests.get(url=url, headers=headers)

        with open(f"data/page_{i}.html", "w", encoding="utf-8") as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count + 1




def main():
    pages_count = get_all_pages()


if __name__ == '__main__':
    main()
