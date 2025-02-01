from flask import Flask, request, jsonify, redirect
from requests import get, post
from dotenv import load_dotenv
import os
from flask_cors import CORS  # Import CORS

load_dotenv()
app = Flask(__name__)

# Enable CORS for React (running on port 3000)
CORS(app)

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read'
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

user_choice = None
access_token = None

@app.route('/')
def home():
    return jsonify({
        "message": "Spotify Downloader. Please select an option.",
        "liked_songs_url": "/authorize?type=liked_songs",
        "saved_playlists_url": "/authorize?type=saved_playlists"
    })

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
        songs_response = get('https://api.spotify.com/v1/me/tracks', headers=headers)
        if songs_response.status_code == 200:
            songs = songs_response.json()
            tracks = songs['items']
            liked_songs = [{"id": track['track']['id'], "name": track['track']['name']} for track in tracks]
            return jsonify(liked_songs)  # Return directly as JSON
        else:
            return jsonify({"error": f"Failed to fetch songs. {songs_response.status_code} {songs_response.text}"}), 400

    elif user_choice == "saved_playlists":
        albums_response = get('https://api.spotify.com/v1/me/playlists', headers=headers)
        albums_response_json = albums_response.json()
        albums = albums_response_json['items']
        playlists = [{"id": album['id'], "name": album['name']} for album in albums]
        return jsonify(playlists)  # Return directly as JSON

if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Ensure Flask runs on port 5000
