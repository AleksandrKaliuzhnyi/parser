url = "https://www.securitylab.ru/news/525065.php"

#article_id = url.split("/")[-1].split(".")[0]
article_id = url.split("/")[-1]
article_id = article_id[:-4]

print(article_id)