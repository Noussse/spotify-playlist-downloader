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

import json

def reading_and_downloading_all_the_songs():
    try:
        print("Starting download process...")
        # Open and load the JSON data from the file
        with open("liked_songs.txt", "r", encoding="utf-8") as f:
            songs = json.load(f)

        total_songs = len(songs)
        print(f"Found {total_songs} songs to download")

        # Iterate over each song in the list
        for index, song in enumerate(songs, 1):
            song_name = song['name']
            artist_name = song['artist']
            song_query = f'"{song_name}" by {artist_name}'

            print(f"\nProcessing song {index}/{total_songs}: {song_query}")
            
            # Search for the song on YouTube
            video_url = search_youtube(song_query)
            
            if video_url:
                print(f"Found video URL: {video_url}")
                download_youtube_audio(video_url)
            else:
                print(f"Skipping download for: {song_query} (no video found)")

    except FileNotFoundError:
        print("Error: liked_songs.txt file not found")
        raise
    except json.JSONDecodeError:
        print("Error: liked_songs.txt is not valid JSON")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise


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


