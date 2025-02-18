import { useState, useRef, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const wsRef = useRef(null)
  const imageRef = useRef(null);

  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://127.0.0.1:8000/ws');

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
      };

      ws.onmessage = (e) => {
        if (imageRef.current) {
          imageRef.current.src = event.data;
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
      </div>
    </div>
  )
}

export default App
