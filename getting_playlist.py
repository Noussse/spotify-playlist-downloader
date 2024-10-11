from requests import get, post
from dotenv import load_dotenv
import os
import webbrowser
from flask import Flask, request, redirect

load_dotenv()
app = Flask(__name__)

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read'
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

user_choice = None
access_token = None

@app.route('/')
def home():
    return """
        <h1>Spotify Downloader</h1>
        <h2>Please select an option:</h2>
        <a href="/authorize?type=liked_songs">Download Liked Songs</a><br>
        <a href="/authorize?type=saved_playlists">Download Saved Playlists</a>
    """

@app.route('/authorize')
def authorize():
    global user_choice
    user_choice = request.args.get('type')
    return redirect(auth_url)

@app.route('/callback')
def callback():
    global access_token
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = post(token_url, data=data)
    tokens = response.json()
    access_token = tokens.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}

    if user_choice == "liked_songs":
        return register_songs('https://api.spotify.com/v1/me/tracks')
    elif user_choice == "saved_playlists":
        return display_playlists(headers)

def register_songs(url):
    songs_response = get(url, headers={'Authorization': f'Bearer {access_token}'})
    if songs_response.status_code == 200:
        songs = songs_response.json()
        tracks = songs['items']

        with open('liked_songs.txt', 'w', encoding='utf-8') as f:
            for track in tracks:
                f.write(f"{track['track']['name']} by {track['track']['artists'][0]['name']}\n")

        return "Songs saved to (liked_songs.txt) for the download to start lunch 'searching_and_downloading_from_youtube.py'. You can close this window."
    else:
        return f"Failed to fetch songs. {songs_response.status_code} {songs_response.text}"

def display_playlists(headers):
    albums_response = get('https://api.spotify.com/v1/me/playlists', headers=headers)
    albums_response_json = albums_response.json()
    albums = albums_response_json['items']

    # Create links for each playlist
    playlist_html = "<h2>Your Playlists:</h2><ul>"
    for album in albums:
        playlist_id = album['id']
        playlist_name = album['name']
        playlist_html += f'<li><a href="/download_playlist?playlist_id={playlist_id}">{playlist_name}</a></li>'
    playlist_html += "</ul>"

    return playlist_html

@app.route('/download_playlist')
def download_playlist():
    playlist_id = request.args.get('playlist_id')
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    return register_songs(url)

if __name__ == '__main__':
    webbrowser.open('http://localhost:5000/')
    app.run(port=5000, debug=True)
