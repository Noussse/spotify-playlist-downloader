from flask import Flask, request, redirect, jsonify, session
from requests import post, get
from flask_cors import CORS 
import os
import json
from searching_and_downloading_from_youtube import reading_and_downloading_all_the_songs
app = Flask(__name__)

app.secret_key = os.urandom(24)


CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read'
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

@app.route('/authorize')
def authorize():
    return redirect(auth_url)

@app.route('/callback')
def callback():
    #exchanging code with token
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
    
    if access_token:
        session['access_token'] = access_token
        session.permanent = True
        return redirect(f'http://localhost:5173/?login=success')
    else:
        return jsonify({"error": "Failed to obtain access token"}), 400

@app.route('/get_token')
def get_token():
    access_token = session.get('access_token')
    if access_token:
        return jsonify({"access_token": access_token})
    return jsonify({"error": "No access token found"}), 401

@app.route('/liked_songs')
def get_liked_songs():
    url = 'https://api.spotify.com/v1/me/tracks'
    downloadsong(url)


def downloadsong(url):
    access_token = session.get('access_token')

    if not access_token:
        return jsonify({"error": "Access token is missing or expired"}), 401
    
    songs_response = get(url, headers={'Authorization': f'Bearer {access_token}'})
    
    if songs_response.status_code == 200:
        songs = songs_response.json()
        tracks = [
            {"name": track['track']['name'], "artist": track['track']['artists'][0]['name']}
            for track in songs['items']
        ]
        # Save to file
        with open('liked_songs.txt', 'w', encoding='utf-8') as f:
            json.dump(tracks, f, indent=4)

        try:
            reading_and_downloading_all_the_songs()
            return jsonify({"tracks": tracks, "message": "Download process started"})
        except Exception as e:
            return jsonify({"tracks": tracks, "error": str(e)}), 500
    else:
        return jsonify({"error": "Failed to fetch songs"}), songs_response.status_code

@app.route('/get_playlist_names')
def getplaylist():
    access_token = session.get('access_token')
    headers = {"Authorization": f"Bearer {access_token}"}

    url = 'https://api.spotify.com/v1/me/playlists'
    response =get(url, headers=headers)

    if response.status_code == 200:
        playlists = response.json()['items']
        playlist_names = [
            {'id': playlist['id'], 'name': playlist['name']}
            for playlist in playlists
        ]
        return jsonify(playlist_names)
    else:
        return jsonify({"error": "Failed to fetch playlists"}), response.status_code
    
@app.route('/download_playlist')
def downloadplaylist():
    playlist_id = request.args.get('playlist_id')
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    return downloadsong(url)



if __name__ == '__main__':
    app.run(port=5000, debug=True)