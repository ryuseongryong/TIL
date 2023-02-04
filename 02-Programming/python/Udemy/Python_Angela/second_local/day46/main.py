import os, requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.chdir("./Udemy/Python_Angela/second_local/day46")
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)

res = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(res.text, "html.parser")
song_name_spans = soup.find_all("span", class_="a-no-trucate")
song_names = [song.getText() for song in song_name_spans]

# ----------------------------------------------------------------------------------------

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]
song_uris = []

year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
