from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import cv2
import base64
import asyncio
import uvicorn
from Zed_class import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Attempting to accept websocket connection")
    await websocket.accept()
    print("Websocket connection accepted\n")
    try:
        zed = ZEDCamera()
        zed.configure_camera()
        zed.open_camera()
        while True:
            frame = zed.single_frame_inference(True)["frame"]
            _, buffer = cv2.imencode('.jpg', frame)
            base64_frame = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_text(f"data:image/jpeg;base64,{base64_frame}")
            await asyncio.sleep(0.033) # 30 FPS
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
