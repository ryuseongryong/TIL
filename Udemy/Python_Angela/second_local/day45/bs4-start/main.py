import os
from bs4 import BeautifulSoup
import lxml

os.chdir("./Udemy/Python_Angela/second_local/day45/bs4-start")

import requests

res = requests.get("https://news.ycombinator.com/news")
yc_web_page = res.text

soup = BeautifulSoup(yc_web_page, "html.parser")
# print(yc_webs_page)
# print(soup.title)
articles = soup.find_all(name="span", class_="titleline").find_all(name="a")
article_texts = []
article_links = []
for article_tag in articles:
    text = article_tag.getText()
    article_texts.append(text)
    link = article_tag.get("href")
    article_links.append(link)

article_upvote = [
    score.getText() for score in soup.find_all(name="span", class_="score")
]
print(article_texts)
print(article_links)
print(article_upvote)


# -------------------------------------------------------------------------------------------------------- #
# with open("website.html") as file:
#     contents = file.read()

# # soup = BeautifulSoup(contents, "lxml")
# soup = BeautifulSoup(contents, "html.parser")
# # print(soup.title)
# # print(soup.title.string)

# # print(soup.prettify())

# # print(soup.p)

# all_anchor_tags = soup.find_all(name="a")
# # print(all_anchor_tags)

# for tag in all_anchor_tags:
#     # print(tag.getText())
#     # print(tag.get("href"))
#     pass

# heading = soup.find(name="h1", id="name")
# # print(heading)

# section_heading = soup.find(name="h3", class_="heading")
# # print(section_heading.getText())
# # print(section_heading.get("class"))

# class_is_heading = soup.find_all(class_="heading")
# print(class_is_heading)

# h3_heading = soup.find_all("h3", class_="heading")
# print(h3_heading)

# name = soup.select_one(selector="#name")
# print(name)

# headings = soup.select(".heading")
# print(headings)
