import React, { useState } from 'react';

const SpotifyDownloader = () => {
    const [playlists, setPlaylists] = useState([]);
    const [likedSongs, setLikedSongs] = useState([]);

    // Function to handle downloading liked songs
    const handleLikedSongs = async () => {
        // This triggers the redirect to Spotify authorization
        const response = await fetch('http://localhost:5000/authorize?type=liked_songs');
        if (response.ok) {
            // You need to handle the flow and response properly
            console.log('Successfully authorized for liked songs.');
        } else {
            console.error('Failed to fetch liked songs');
        }
    };

    // Function to handle downloading saved playlists
    const handleSavedPlaylists = async () => {
        // This triggers the redirect to Spotify authorization
        const response = await fetch('http://localhost:5000/authorize?type=saved_playlists');
        if (response.ok) {
            console.log('Successfully authorized for playlists.');
        } else {
            console.error('Failed to fetch playlists');
        }
    };

    return (
        <div>
            <h1>Spotify Downloader</h1>
            <h2>Please select an option:</h2>
            <button onClick={handleLikedSongs}>Download Liked Songs</button>
            <button onClick={handleSavedPlaylists}>Download Saved Playlists</button>

            <div>
                <h2>Your Playlists:</h2>
                <ul>
                    {playlists.map((playlist) => (
                        <li key={playlist.id}>{playlist.name}</li>
                    ))}
                </ul>
            </div>

            <div>
                <h2>Your Liked Songs:</h2>
                <ul>
                    {likedSongs.map((song) => (
                        <li key={song.id}>{song.name}</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default SpotifyDownloader;
