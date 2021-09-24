import requests
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


def get_source_html(url):
    driver = webdriver.Chrome(
        executable_path="D:\Python\parser\parser_6\chromedriver\chromedriver.exe"
    )

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)

        while True:
            find_more_element = driver.find_element_by_class_name("catalog-button-showMore")

            if driver.find_elements_by_class_name("hasmore-text"):
                with open("sourse-page.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)

                break
            else:
                # scrolling before block "hasmore-text" will be found
                action = ActionChains(driver)
                action.move_to_element(find_more_element).perform()
                time.sleep(3)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

def get_items_urls(file_path):
    with open(file_path, encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    items_divs = soup.find_all("div", class_="service-description")

    urls = []
    for item in items_divs:
        item_url = item.find("div", class_="H3").find("a").get("href")
        urls.append(item_url)

    with open("items_urls.txt", "w", encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collected successfully!"


def main():
    #get_source_html(url="https://spb.zoon.ru/medical/?search_query_form=1&m%5B5200e522a0f302f066000055%5D=1&center%5B%5D=59.91878264665887&center%5B%5D=30.342586983263384&zoom=10")
    print(get_items_urls(file_path="D:\Python\parser\parser_6\sourse-page.html"))


if __name__ == '__main__':
    main()
