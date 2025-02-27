import { useState, useRef, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const ACTION_LABELS = {
  0: "Jab Orthodox",
  1: "Jab Southpaw",
  2: "Cross Orthodox",
  3: "Cross Southpaw",
  4: "Lead Hook Orthodox",
  5: "Lead Hook Southpaw",
  6: "Rear Hook Orthodox",
  7: "Rear Hook Southpaw",
  8: "Lead Upper Orthodox",
  9: "Lead Upper Southpaw",
  10: "Rear Upper Orthodox",
  11: "Rear Upper Southpaw",
  12: "Guard",
  13: "Idle"
}

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const wsRef = useRef(null)
  const imageRef = useRef(null);
  const [processedActions, setProcessedActions] = useState([]);

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

	// Sets the estimations
	if (data.estimations) {
	  console.log(data.estimations);
	  const parsedArray = JSON.parse(data.estimations);

	  const formattedActions = parsedArray.map((item, idx) => {
	    return {
	      actionId: idx,
	      confidence: Math.floor(parseFloat(item * 100)),
	      label: ACTION_LABELS[idx],
	    };
	  });

	  console.log(formattedActions);
	  setProcessedActions(formattedActions);
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

	  <p className="font-semibold text-8xl">On-Hit</p>

	  {!isConnected && (<p>Connecting to camera..</p>)}
	  {error && (<p>Error: {error}</p>)}
	  
	  <img ref={imageRef} className="w-full h-full object-contain" />

	  {processedActions.map(action => (
	    <div key={action.actionId} >
	      <p className="text-3xl">{action.label} - {action.confidence}%</p>
	    </div>
	  ))}

      </div>
    </div>
  )
}

export default App
