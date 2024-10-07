# Spotify Liked Songs Downloader

A Python-based tool that allows users to download their liked songs from Spotify and fetch the corresponding audio from YouTube. This project integrates with the Spotify API to retrieve your liked songs and uses YouTube for downloading audio files.

## Features

- **Spotify API Integration**: Authenticate and retrieve your liked songs.
- **YouTube Search and Download**: Finds and downloads songs from YouTube.
- **FFmpeg Integration**: Processes and converts downloaded audio files.
- **File Management**: Saves liked songs into a text file for easy reference.
- **Flask Web Server**: Simple web server for handling Spotify OAuth2 authentication.

## Installation

### Prerequisites

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/download.html) (for audio processing)
- A Spotify Developer account
- A YouTube API Key (for searching songs on YouTube)

### Libraries

Install the required Python dependencies:

```bash
pip install flask requests python-dotenv yt-dlp
```
## Setting up Environment Variables

Create a `.env` file in the root of your project and add the following keys:

```env
client_id=your_spotify_client_id
client_secret=your_spotify_client_secret
youtube_apikey=your_youtube_api_key
```
## all files explanation :

- env :
 Contains client ID, secret, and YouTube API key

 - GettingPlaylist.py :
 Main script for handling the Spotify API and Flask server

- searching_in_youtube.py :
Script for searching and downloading songs from YouTube

- liked_songs.txt
:File where liked songs from Spotify are stored(the file will be created after runing GettingPlaylist.py for the first time)

### run GettingPlaylist.py to get the songs names in liked_songs.txt then stop the flask server and run searching_in_youtube.py after all the songs are downloaded you will find them in your "downloads" folder in a folder called "songfixer"



 
