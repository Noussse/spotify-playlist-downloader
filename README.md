# 🎵 Spotify Playlist Downloader 🎧

## 📌 Project Overview

A full-stack web application that allows users to download their Spotify liked songs and playlists with ease, leveraging the Spotify API and YouTube for music retrieval.

## ✨ Features

- 🔐 Secure Spotify Authentication
- 📥 Download Liked Songs
- 🎼 Download Specific Playlists
- 🔍 Intelligent YouTube Search Integration
- 🎧 MP3 Audio Extraction

## 🛠 Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

### Backend
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### APIs
![Spotify API](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)
![YouTube API](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Spotify Developer Account
- YouTube API Key
- `yt-dlp` installed for audio downloading

# Installation

## 1. Clone the repository
```bash
git clone https://github.com/Noussse/spotify-playlist-downloader
cd spotify-playlist-downloader
```
## 2.Set up Backend
### Create virtual environment
```bash
python -m venv venv
source venv\Scripts\activate
```
### Install dependencies
```bash
pip install flask requests python-dotenv yt-dlp
```
## 3.Set up Frontend
```bash
npm create vite@latest my-app --template react
cd my-app
npm install
npm run dev
```
## 🔐 API Setup
### Spotify API

1.Go to Spotify Developer Dashboard

2.Create a new app

3.Set redirect URI to http://localhost:5000/callback

4.Copy Client ID and Client Secret

### YouTube API

1.Go to Google Cloud Console

2.Create a new project

3.Enable YouTube Data API v3

4.Create credentials (API Key)

### 📦 Environment Variables
-Create .env file:
```bash
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_APIKEY=your_youtube_api_key
```
## 🤖 How It Works

1. **Authenticate with Spotify**
2. **Fetch your liked songs or playlists**
3. **For each song:**
   - Search YouTube using song and artist name
   - Download the first matching video as MP3
4. **Save MP3 files to `~/Downloads/musicfixer/`**

## 🧩 Key Components

### Backend Scripts

#### `searching_and_downloading_from_youtube.py`
- Searches YouTube for song matches
- Handles YouTube API requests
- Downloads audio using `yt-dlp`

**Key Functions:**
- `search_youtube(song_name)`: Finds YouTube video URL
- `reading_and_downloading_all_the_songs()`: Downloads entire song list
- `download_youtube_audio(video_url)`: Extracts MP3 audio

### Frontend Components
- Spotify authentication
- Playlist and liked songs browsing
- Download initiation

## 🛡 Security

- Secure token management
- CORS protection
- Environment variable configuration
- API quota management

## 🚧 Known Limitations

- Downloads depend on YouTube search accuracy
- Limited by YouTube API quota
- Requires active internet connection
- Some songs might not have exact matches


## 📦 Dependencies

- Flask
- React
- Requests
- yt-dlp
- python-dotenv
- Flask-CORS

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🚨 Disclaimer

This tool is for personal use. Respect copyright laws and streaming service terms of service.

⭐ **Don't forget to star the repository if you found it helpful!** 🎉
