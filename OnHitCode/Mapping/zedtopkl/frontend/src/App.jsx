import { useState, useRef, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const wsRef = useRef(null)
  const imageRef = useRef(null);
  const [keypoints, setKeypoints] = useState('');

  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://127.0.0.1:8000/ws');

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
      };

      ws.onmessage = (e) => {
	const data = JSON.parse(e.data);

	// Sets the image
        if (imageRef.current && data.image) {
          imageRef.current.src = data.image;
	}

	// Sets the keypoints
	if (data.keypoints) {
	  setKeypoints(data.keypoints);
	}

      }

      ws.onerror = (e) => {
	setError("Failed to connect");
	setIsConnected(false);
      };

      ws.onclose = () => {
	setIsConnected(false);
	setTimeout(connectWebSocket, 3000);
      };

      wsRef.current = ws;
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
	wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="flex flex-row justify-center py-[5rem]">
      <div className="flex flex-col justify-center items-center">
	  <p className="font-bold text-4xl">On-Hit</p>
	  {!isConnected && (<p>Connecting to camera..</p>)}
	  {error && (<p>Error: {error}</p>)}
	  <img ref={imageRef} className="w-full h-full object-contain" />
	  {keypoints && (
	    <div className="flex flex-col items-center">
	      <p>ID: {keypoints[0]?.id}</p>
	    </div>
	)}
      </div>
    </div>
  )
}

export default App
