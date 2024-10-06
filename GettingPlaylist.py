from requests import get, post
from dotenv import load_dotenv
import os
import webbrowser
from flask import Flask, request
load_dotenv()
app = Flask(__name__)
with open('liked_songs.txt', 'w') as f:
    pass

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read'
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

@app.route('/')
def home():
    return "Please authorize the application."

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response =post(token_url, data=data)
    tokens = response.json()
    access_token=tokens.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    liked_songs_response = get('https://api.spotify.com/v1/me/tracks', headers=headers)
    if liked_songs_response.status_code == 200:
        liked_songs = liked_songs_response.json()
        tracks = liked_songs['items']
        with open('liked_songs.txt', 'w') as f:
            for track in tracks:
                f.write(f"{track['track']['name']} by {track['track']['artists'][0]['name']}\n")
        return "Songs saved to (liked_songs.txt) and will start downloading soon You can close this window."
    else :
        return f"Failed to fetch liked songs.{liked_songs_response.status_code}{liked_songs_response.text}"



if __name__ == '__main__':
    webbrowser.open(auth_url)
    app.run(port=5000, debug=True)