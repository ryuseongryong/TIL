import os
from bs4 import BeautifulSoup
import lxml

os.chdir("./Udemy/Python_Angela/second_local/day45/bs4-start")


with open("website.html") as file:
    contents = file.read()

# soup = BeautifulSoup(contents, "lxml")
soup = BeautifulSoup(contents, "html.parser")
# print(soup.title)
# print(soup.title.string)

# print(soup.prettify())

print(soup.p)
