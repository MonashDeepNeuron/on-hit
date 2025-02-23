import sys
import pickle
import os
from socket_client import *
import time
import numpy as np

# Get the parent directory
target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Mapping/zedtopkl"))

# Add the sibling directory (dir2) to sys.path
sys.path.append(target_dir)


# Now you can import zedtopkl files
from Zed_class import *
from body34_to_NTU25 import *

zed = ZEDCamera()
zed.configure_camera()
zed.open_camera()

jetson_client = SocketClient()

while True:
    '''
    Main loop
    every 2 seconds record the player,
    convert into ntu skeleton,
    send it to the server
    wait for response repeat
    
    '''
    frames = []
    start_time = time.time()
    while time.time() - start_time < 2:  
        zed_result = zed.single_frame_inference()
        if len(zed_result["keypoints"]):
            frames.append(zed_result["keypoints"][0])


    num_bodies = 1   
    max_frames = len(frames)
    num_joints = 25
    num_cords = 3 #3d skeleton
    # np array in size [M x T x V x C]
    skeleton_array = np.full((num_bodies,max_frames,num_joints,num_cords), np.nan, dtype=np.float32)

    for t,frame in enumerate( frames):

        keypoints = convert_zed34_to_ntu(frame["keypoints"])

        #hard coded
        skeleton_array[0,t] = keypoints 
    
    pickle_data = pickle.dumps(skeleton_array)
    jetson_client.send_message(pickle_data)

    print(jetson_client.receive_message())




