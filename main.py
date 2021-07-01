import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "faadda8616894424ae266268b72fcc9e"
CLIENT_SECRET = "5e8dbdf3db174fa3bbbcb9b48fe9cd0e"
USER_ID = 0
REDIRECT_URI = "https://www.google.com"
# user_input = input("Which year you want to travel to ?"
#                    "\nType the date in YYYY-MM-DD Format\n")
# print(user_input)


# -------------------------------------SCRAPING USING Beautiful SOUP ---------------#
response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12")
web_data = response.text

soup = BeautifulSoup(web_data, "html.parser")

ele_list = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
songs_list = [items.getText() for items in ele_list]

# ---------------------------------AUTHENTICATION WITH SPOTIFY -------------#

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
date = input("Enter the year you want to travel to in format YYYY-MM-DD")

songs_uri = []
year = date.split("-")[0]
for song in songs_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result['tracks']['items'][0]['uri']
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} is not found on Spotify so skipped")

playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} playlist by Rudra", public=False)["id"]
print(playlist_id)
sp.playlist_add_items(playlist_id=playlist_id, items=songs_uri)
