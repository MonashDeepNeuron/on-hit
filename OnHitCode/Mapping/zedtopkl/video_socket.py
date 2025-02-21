# Sets current directory at 'OnHitCode' directory
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import cv2
import base64
import asyncio
import uvicorn
import json
from Mapping.zedtopkl.Zed_class import *
from inference.socket_client import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

zed = ZEDCamera()

@app.on_event("startup")
async def startup_event():
    print("[FASTAPI] Initializing the camera")
    print("[FASTAPI] Configuring the camera..")
    zed.configure_camera()
    print("[FASTAPI] Camera configured, opening the camera..")
    zed.open_camera()
    print("[FASTAPI] Camera opened")

@app.on_event("shutdown")
async def shutdown_event():
    if zed:
        zed.cleanup()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    print("[FASTAPI] Attempting to accept websocket connection")
    await websocket.accept()
    print("[FASTAPI] Websocket connection accepted\n")

    try:
        while True:
            single_frame_instance = zed.single_frame_inference(True)
            frame = single_frame_instance["frame"]
            keypoints = single_frame_instance["keypoints"]

            ws_client = SocketClient("130.194.132.217")
            response = ws_client.send_message("Hello Server!")
            print(f"Response from WS: {response}")
            ws_client.close_socket()

            # Image encoding to base64
            _, buffer = cv2.imencode('.jpg', frame)
            base64_frame = base64.b64encode(buffer).decode('utf-8')

            # This is what the frontend will receive
            data_package = {
                "image": f"data:image/jpeg;base64,{base64_frame}",
                "keypoints": keypoints,
            }
            await websocket.send_text(json.dumps(data_package))

            await asyncio.sleep(0.033) # 30 FPS
    except Exception as e:
        print(f"Error: {str(e)}")
