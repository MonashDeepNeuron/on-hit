import sys
import cv2
import pickle
import os
from socket_client import *
import time
import numpy as np

# Get the parent directory
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Mapping/zedtopkl"))

# Add the sibling directory (dir2) to sys.path
sys.path.append(target_dir)


# Importanting the relevant files from with zedtopkl
from Zed_class import *
from body34_to_NTU25 import *

#Initating our zed camera object
zed = ZEDCamera()
zed.configure_camera()
zed.open_camera()

jetson_client = SocketClient()
key_wait = 10

'''
Press s, and then start recording
After 2 seconds, you stop recording and add the zed skeleton into a list 
iterate throught the list and convert them into ntu-skeleton
add the skeleton into the correct format for the stgcn prediction
turn it into a pickle and then, send it over the packet
wait to recieve predictions
print results

'''
while True:

    server_socket, server_address = jetson_client.client_socket.accept()
    while True:
        print(f"Connected by {server_address}")


        buffer = b""
        while True:
        # Receive a single message
            data = server_socket.recv(64)
            buffer += data 
            if b"<END>" in buffer:
                print("Buffer reached")
                break
        #Gotta remove the buffer
        cleaned_data, _ = buffer.split(b"<END>",1)
        if input("Press 's' to start: ") == "s":
            frames = []
            start_time = time.time()
            
            # Record for 2 seconds
            while time.time() - start_time < 2:
                zed_result = zed.single_frame_inference(False)
                if len(zed_result["keypoints"]):
                    frames.append(zed_result["keypoints"][0])

            #video_frame = zed_result["frame"]

            #cv2.imshow("Zed", video_frame)

            num_bodies = 1   
            max_frames = len(frames)
            num_joints = 25
            num_cords = 3  # 3D skeleton
            skeleton_array = np.full((num_bodies, max_frames, num_joints, num_cords), np.nan, dtype=np.float32)

            # Convert skeleton data
            for t, frame in enumerate(frames):
                keypoints = convert_zed34_to_ntu(frame["keypoints"])
                skeleton_array[0, t] = keypoints 

            # Prepare Pickle Data
            annotations = {
                'frame_dir': "test_name",
                'label': 0,
                'total_frames': max_frames,
                'keypoint': skeleton_array
            }

            pickle_data = pickle.dumps(annotations) 
            jetson_client.send_message(pickle_data)  # Send Data
            print("📤 Data sent. Waiting for response...")

            buffer = b""
            while True:
            # Receive a single message
                data = server_socket.recv(64)
                buffer += data 
                if b"<END>" in buffer:
                    print("Buffer reached")
                    break
            #Gotta remove the buffer
            cleaned_data, _ = buffer.split(b"<END>",1)
            print(f"📥 Server Response: {cleaned_data}")
