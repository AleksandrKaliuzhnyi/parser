import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
}


start_time = time.time()


def get_data():
    cur_time = datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"labirint_{cur_time}.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Book name",
                "Author",
                "Publishing",
                "Sale price",
                "Price",
                "Sale amount",
                "Status"
            )
        )

    url = "https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table"

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response, 'lxml')

    pages_count = int(soup.find("div", class_="pagination_numbers").find_all("a")[-1].text)

    books_data = []
    for page in range(1, pages_count + 1):
        url = f"https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table={page}"

        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response, "lxml")

        books_items = soup.find("tbody", class_="products-table__body").find_all("tr")

        for bi in books_items:
            book_data = bi.find_all("td")

            try:
                book_title = book_data[0].find("a").text.strip()
            except:
                book_title = "No book title"

            try:
                book_author = book_data[1].find("a").text.strip()
            except:
                book_author = "No book author"

            try:
                book_publishing = book_data[2].find("a")
                book_publishing = ":".join([bp.text for bp in book_publishing])
            except:
                book_publishing = "No book publishing"

            try:
                book_new_price = int(book_data[3].find("div", class_="price").find("span").find("span").text.strip().replace(" ", ""))
            except:
                book_new_price = "No new book price"

            try:
                book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
            except:
                book_old_price = "No old book price"

            try:
                book_sale = round(((book_old_price - book_new_price) / book_old_price) * 100)
            except:
                book_sale = "No sales"

            try:
                book_status = book_data[-1].text.strip()
            except:
                book_status = "No book status"

            books_data.append(
                {
                    "book_title": book_title,
                    "book_author": book_author,
                    "book_publishing": book_publishing,
                    "book_new_price": book_new_price,
                    "book_old_price": book_old_price,
                    "book_sale": book_sale,
                    "book_status": book_status
                }
            )

            with open(f"labirint_{cur_time}.csv", "a", encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )

        print(f"Page {page}/{pages_count} finished!")
        time.sleep(1)

    with open(f"labirint_{cur_time}.json", "w", encoding="utf-8") as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f"Time spent - {finish_time}")


if __name__ == "__main__":
    main()
