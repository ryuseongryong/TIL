import os, requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

os.chdir("./Udemy/Python_Angela/second_local/day46")
load_dotenv()

# date = input(
#     "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
# )

# res = requests.get("https://www.billboard.com/charts/hot-100/" + date)

# soup = BeautifulSoup(res.text, "html.parser")
# song_name_spans = soup.find_all("span", class_="a-no-trucate")
# song_name = [song.getText() for song in song_name_spans]

# ----------------------------------------------------------------------------------------

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-read-private",
        redirect_uri="https://example.com/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]
print(user_id)
