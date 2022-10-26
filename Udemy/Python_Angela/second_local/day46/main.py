import os, requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.chdir("./Udemy/Python_Angela/second_local/day46")
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# Scraping Billboard 100
date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.find_all("span", class_="chart-element__information__song")
song_names = [song.getText() for song in song_names_spans]

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# Searching Spotify for songs by title
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

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(
    user=user_id, name=f"{date} Billboard 100", public=False
)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# date = input(
#     "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
# )

# res = requests.get("https://www.billboard.com/charts/hot-100/" + date)

# soup = BeautifulSoup(res.text, "html.parser")
# song_name_spans = soup.find_all("span", class_="a-no-trucate")
# song_name = [song.getText() for song in song_name_spans]

# # ----------------------------------------------------------------------------------------


# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="playlist-modify-private",
#         redirect_uri="https://example.com/callback",
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         show_dialog=True,
#         cache_path="token.txt",
#     )
# )
# user_id = sp.current_user()["id"]
# date = input(
#     "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
# )
# song_uris = []

# year = date.split("-")[0]
# for song in song_names:
#     result = sp.search(q=f"track:{song} year:{year}", type="track")
#     print(result)
#     try:
#         uri = result["tracks"]["items"][0]["uri"]
#         song_uris.append(uri)
#     except IndexError:
#         print(f"{song} doesn't exist in Spotify. Skipped.")
