from flask import Flask, request, jsonify, redirect
from requests import post
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private user-library-read'
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

access_token = None



@app.route('/authorize')
def authorize():
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

    return redirect(f'http://localhost:5173/?access_token={access_token}')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
