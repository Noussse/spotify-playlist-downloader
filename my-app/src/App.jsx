import React, { useState, useEffect } from 'react';

function App() {
  const [accessToken, setAccessToken] = useState(null);
  const [songs, setSongs] = useState([]);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('login') === 'success') {
      fetchToken();
    }
  }, []);

  const fetchToken = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_token', {
        credentials: 'include'  // Important: include credentials
      });
      const data = await response.json();
      if (response.ok) {
        setAccessToken(data.access_token);
      }
    } catch (error) {
      console.error("Error fetching token:", error);
    }
  };

  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/authorize';
  };

  const downloadLikedSongs = async () => {
    try {
      const response = await fetch('http://localhost:5000/liked_songs', {
        credentials: 'include'  
      });
      const data = await response.json();
      
      if (response.ok) {
        setSongs(data.tracks);
        console.log("Liked Songs:", data.tracks);
        // Show message to user about download starting
        alert("Songs are being downloaded to your Downloads/musicfixer folder!");
        if (data.error) {
          console.error("Download error:", data.error);
        }
      } else {
        console.error("Error fetching songs:", data.error);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
  };

  return (
    <div className="App">
      <h1>Spotify Login</h1>
      {accessToken ? (
        <div>
          <button onClick={downloadLikedSongs}>Download liked songs</button>
          <div>
            {songs.map((song, index) => (
              <div key={index}>
                {song.name} - {song.artist}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <button onClick={handleLogin}>Login with Spotify</button>
      )}
    </div>
  );
}

export default App;
