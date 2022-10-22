import os, requests
from bs4 import BeautifulSoup

os.chdir("./Udemy/Python_Angela/second_local/day46")

date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)

res = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(res.text, "html.parser")
song_name_spans = soup.find_all("span", class_="a-no-trucate")
song_name = [song.getText() for song in song_name_spans]
