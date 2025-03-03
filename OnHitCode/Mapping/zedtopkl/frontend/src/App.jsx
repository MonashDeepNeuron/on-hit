import { useState, useRef, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import sphereLogo from '/sphere.svg'
import star from '/star.svg'
import donut from '/donut.svg'
import hpcLogo from '/hpc_logo.svg'
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

const ProgressBar = ({ action }) => {
  const [confidence, setConfidence] = useState(0);

  useEffect(() => {
    setConfidence(action?.confidence);
  }, [action?.confidence]);

  const progressStyle = {
    width: `${confidence}%`,
    backgroundColor: '#4f46e5',
    transition: 'width 50ms ease-in-out'
  };

  return (
    <div className="w-full flex flex-col py-6">
      <div className="text-6xl font-medium pb-3">
	{action.label}
      </div>

      <div className="relative w-full bg-neutral-200 rounded-3xl h-[3rem]">
	<div className="flex items-center justify-center text-black text-4xl">{action?.confidence}%</div>
	<div className="absolute top-0 left-0 z-1 rounded-3xl h-full" style={progressStyle}></div>
      </div>

    </div>
  );
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

	  formattedActions.sort((a, b) => b.confidence - a.confidence);

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
    <div className="relative flex h-screen flex-row justify-center bg-[url(/mdn_gradient.png)] text-white">

      <img className="absolute -bottom-80 -left-40 w-300 h-300" src={sphereLogo} />
      <img className="absolute bottom-60 left-200 w-25 h-55" src={star} />
      <img className="absolute -top-50 -right-70 w-300 h-300" src={donut} />
      <img className="absolute -bottom-50 right-0 w-200 h-200" src={hpcLogo} />

      <div className="flex flex-col pt-[15rem] justify-items-start w-3/4">

	  <p className="font-semibold text-[12rem] pb-3 flex flex-row justify-center">On-Hit</p>

	  {!isConnected && (<p>Connecting to camera..</p>)}
	  {error && (<p>Error: {error}</p>)}
	  
	  <div className="flex flex-row w-auto justify-between gap-x-[3rem]">
	    <img ref={imageRef} className="w-full object-contain overflow-hidden rounded-3xl" />

	    <div className="flex flex-col w-1/4">
	    {processedActions.slice(0, 5).map(action => (
	      <ProgressBar action={action} />
	    ))}
	    </div>
	  </div>

      </div>
    </div>
  )
}

export default App
