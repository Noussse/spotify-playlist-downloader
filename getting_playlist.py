from requests import get, post
from dotenv import load_dotenv
import os
import webbrowser
from flask import Flask, request,redirect
load_dotenv()
app = Flask(__name__)
with open('liked_songs.txt', 'w') as f:
    pass

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read'
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
user_choice=None
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
    # Get the user's choice from the query parameter
    user_choice = request.args.get('type')
    # Redirect to Spotify for authorization
    return redirect(auth_url)

@app.route('/callback')
def callback():
    #getting the code to exchange for the token
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    #getting the token
    response =post(token_url, data=data)
    tokens = response.json()
    access_token=tokens.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    liked_songs_url='https://api.spotify.com/v1/me/tracks'

    #a function that downloads songs in a playlist you just need to provide the url to the playlist(api version)
    def register_songs(url):
        songs_response = get(url, headers=headers)
        if songs_response.status_code == 200:
            songs = songs_response.json()
            tracks = songs['items']
            with open('liked_songs.txt', 'w') as f:
                for track in tracks:
                    f.write(f"{track['track']['name']} by {track['track']['artists'][0]['name']}\n")
            return "Songs saved to (liked_songs.txt) and will start downloading soon You can close this window."
        else :
            return f"Failed to fetch liked songs.{songs_response.status_code}{songs_response.text}"
        

    if user_choice=="liked_songs" :
        result_message=register_songs(liked_songs_url)
        return result_message
    elif user_choice=="saved_playlists":
        albums_response=get('https://api.spotify.com/v1/me/playlists',headers=headers)
        albums_response_json=albums_response.json()
        albums_number=albums_response_json['total']
        albums=albums_response_json['items']
        return albums



if __name__ == '__main__':
    webbrowser.open('http://localhost:5000/')
    app.run(port=5000, debug=True)