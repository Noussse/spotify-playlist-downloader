import React, { useState, useEffect } from 'react';

function App() {
  //declaring variables
  const [accessToken, setAccessToken] = useState(null);
  const [songs, setSongs] = useState([]);
  const[playlistNames ,setplaylist]=useState([]);
  const [loading, setLoading] = useState(false); 

  //checking if the backend has the token
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('login') === 'success') {
      fetchToken();
    }
  }, []);
  //if the backend has the token get it 
  const fetchToken = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_token', {
        credentials: 'include',
      });
      const data = await response.json();
      if (response.ok) {
        setAccessToken(data.access_token);
      }
    } catch (error) {
      console.error('Error fetching token:', error);
    }
  };

  //go to /auth to get the login acess
  const handleLogin = () => {
    window.location.href = 'http://localhost:5000/authorize';
  };

  //when clicked tell the backend to download the liiked songs playlist
  const downloadLikedSongs = async () => {
    setLoading(true); 

    try {
      const response = await fetch('http://localhost:5000/liked_songs', {
        credentials: 'include',
      });

      const data = await response.json();

      if (response.ok) {
        setSongs(data.tracks);
        console.log('Liked Songs:', data.tracks);
        alert('Songs are downloaded in your Downloads/musicfixer folder!');
      } else {
        console.error('Error fetching songs:', data.error);
      }
    } catch (error) {
      console.error('Network error:', error);
    } finally {
      setLoading(false); 
    }
  };

  // get all the user playlist names
  const getplaylistnames=async() =>{
    try {
      const response = await fetch('http://localhost:5000/get_playlist_names', {
        credentials: 'include',
      });

      const data = await response.json();

      if (response.ok) {
        setplaylist(data);
        console.log(data)
      } 

      else {
        console.error('Error fetching playlist names:', data.error);
      }

    } 
    catch (error) {
      console.error('Network error:', error);
    } 
  };
  //download a playlist of the user choice
  const downloadplaylist = async (playlistId) => {
    setLoading(true);
    
    try {
      const response = await fetch(`http://localhost:5000/download_playlist?playlist_id=${playlistId}`, {
        credentials: 'include',
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSongs(data.tracks);
        alert('Playlist songs are downloaded in your Downloads/musicfixer folder!');
      } else {
        console.error('Error downloading playlist:', data.error);
      }
    } catch (error) {
      console.error('Network error:', error);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="App">
      <h1>Spotify Login</h1>


      {accessToken ? (
        <div>
          <button onClick={downloadLikedSongs} disabled={loading}>
            {'Download liked songs'}
          </button>

          <button onClick={getplaylistnames} disabled={loading}>
            choose playlist
          </button>



          <div>
          {playlistNames.map((playlist, index) => (
              <div key={index}>
              <a href="#!" onClick={(e) => {e.preventDefault();downloadplaylist(playlist.id);}}>
              {playlist.name}
              </a>
              <br />
          </div>
          ))}
          </div>

          {loading && <p>Downloading songs, please wait...</p>}

          <div>
            {songs.map((song, index) => (
              <div key={index}>
                <p>you successfully downloaded :</p>
                {song.name} - {song.artist}
              </div>
            ))}
          </div>
        </div>
      ) 
      
      :(<button onClick={handleLogin}>Login with Spotify</button>)
      }
    </div>
  );
}

export default App;
