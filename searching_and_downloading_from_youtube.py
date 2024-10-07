from requests import get
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()
api_key = os.getenv("youtube_apikey")
url = "https://www.googleapis.com/youtube/v3/search"

def search_youtube(song_name):
    params = {
        'part': 'snippet',
        'q': song_name,
        'key': api_key,
        'type': 'video',
        'maxResults': 1
    }
    response = get(url, params=params)
    data = response.json()

    # Check for errors in the response
    if 'error' in data:
        print(f"Error: {data['error']['message']}")
        if "quota" in data['error']['message'].lower():
            print("Quota exceeded. Please wait and try again later.")
        return None
    
    # Print the data for debugging
    print(data)

    # Check if items key exists
    if 'items' in data and data['items']:
        video_id = data['items'][0]['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        print(f"No results found for: {song_name}")
        return None


def reading_and_downloading_all_the_songs():
    with open("liked_songs.txt", "r") as f:
        songs = f.readlines()
    for song in songs:
        song = song.strip()
        video_url = search_youtube(song)
        if video_url:  # Ensure video_url is not None before attempting to download
            download_youtube_audio(video_url)

def download_youtube_audio(video_url):
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'musicfixer')
    os.makedirs(downloads_folder, exist_ok=True)  
    
    # Command to download the audio as MP3
    command = [
        'yt-dlp', 
        '-x',  # Extract audio
        '--audio-format', 'mp3',  # Convert to MP3
        '-o', f'{downloads_folder}/%(title)s.%(ext)s', 
        video_url
    ]
    
    try:
        subprocess.run(command, check=True)
        print("Audio download complete!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

reading_and_downloading_all_the_songs()
