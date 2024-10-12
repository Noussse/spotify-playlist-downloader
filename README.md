# Spotify playlist Downloader

A Python-based tool that allows users to download all the songs in a spotify playlist of their choice in bulk and fetch the corresponding audio from YouTube. This project integrates with the Spotify API to retrieve your liked songs and uses YouTube for downloading audio files.
"the playlist needs to be in your library"

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

 - getting_playlist.py :
 Main script for handling the Spotify API and Flask server

- searching_and_downloading_from_youtube.py :
Script for searching and downloading songs from YouTube

- liked_songs.txt
:File where liked songs from Spotify are stored(the file will be created after runing GettingPlaylist.py for the first time)

### run getting_playlist.py and then choose if you want to download your liked songs or a specific playlist to get the songs names in liked_songs.txt then stop the flask server and run searching_and_downloading_from_youtube.py after all the songs are downloaded you will find them in your "downloads" folder in a folder called "songfixer".
##just keep in mind that 100 songs give or take is the limit per day



 
