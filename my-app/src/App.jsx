import React, { useState, useEffect } from 'react';

function App() {
  const [accessToken, setAccessToken] = useState(null);

  useEffect(() => {
    // Extract token from the URL query parameters
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('access_token');
    
    if (token) {
      setAccessToken(token);  // Update state with the token
    }
  }, []);  // Empty dependency array means this will run only once when the component mounts

  return (
    <div className="App">
      <h1>Spotify Login</h1>
      {
      accessToken ? (
        <div>
          <h2>Access Token: {accessToken}</h2>
        </div>
        ) 
      :(
        <button onClick={handleLogin}>Login with Spotify</button>
      )
      }
    </div>
  );
}

const handleLogin = () => {
  window.location.href = 'http://localhost:5000/authorize';
};

export default App;
