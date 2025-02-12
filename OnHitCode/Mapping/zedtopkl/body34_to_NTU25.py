import numpy as np
import re
import json 
import pickle
import os
from tqdm import tqdm

ZED34_TO_NTU_MAPPING = {
        0:1,
        1:2,
        2:21,
        3:3,
        5:5,
        6:6,
        7:7,
        8:8,
        9:22,
        10:23,
        12:9,
        13:10,
        14:11,
        15:12,
        16:24,
        17:25,
        18:13,
        19:14,
        20:15,
        21:16,
        22:17,
        23:18,
        24:19,
        25:20,
        26:4
        }

def convert_zed34_to_ntu(body_data):
    num_frames = len(body_data)
    ntu_joints = 26

    keypoints = np.zeros((ntu_joints,3), dtype = np.float32)

    for index,kp in enumerate(body_data) :
        
        
        #this iterates through the zed points and maps it to the correct ntu joint location
        if kp == [None,None,None]:
            continue
        elif index in ZED34_TO_NTU_MAPPING:
            ntu_index = ZED34_TO_NTU_MAPPING[index]
            keypoints[ntu_index] = kp 

    max_val = np.max(np.abs(keypoints))
    if max_val > 0:
        keypoints /= max_val

    return keypoints

def strip_trailing_L_number(path):
    match = re.search(r'L(\d+)$', path)
    return int(match.group(1)) if match else None  # Convert to int

def process_zed_file(input_path, output_dir, class_label=0):

    #load zed data 
    with open(input_path) as f:
        raw_data = json.load(f)

    max_body = raw_data["bodies"]
    bodies = {}
     

    for frame in raw_data["pose_data"]:
        
        #bodies in the frame
        id_map = []  
        for t,body in  enumerate(frame):

            bodies_inframe = {}
            #body_id = body['id']
            #assuming your only recording one person, this will always reassign your id to 0 
            body_id = 0 
            
                         

            #will just hard code it such that the id will always be zero,      
            bodies.setdefault(body_id, []).append(body)
    
    num_bodies = raw_data["bodies"]   
    max_frames = max(len(frames) for frames in bodies.values())
    num_joints = 26
    num_cords = 3 #3d skeleton
    # np array in size [M x T x V x C]
    skeleton_array = np.full((num_bodies,max_frames,num_joints,num_cords), np.nan, dtype=np.float32)

    #this converts the the zed sksleton into the ntu skeleton
    for body_id, frames in bodies.items():
        
        for t,frame in enumerate( frames):

            keypoints = convert_zed34_to_ntu(frame["keypoints"])
            skeleton_array[body_id,t] = keypoints 
    base_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"

    return {
    'frame_dir': base_name,
    'total_frames': max_frames,
    'keypoint':skeleton_array, 
    'label': class_label
    }

def batch_process(input_dir,output_dir):
    #process all the zed json files in a dir
    annotations = []
    train = []
    val = []
    test = []

    os.makedirs(output_dir,exist_ok=True)

    for file_name in tqdm(os.listdir(input_dir)):
        if not file_name.endswith('.json'):
            continue 

        input_path = os.path.join(input_dir, file_name)
        base_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"
        label = strip_trailing_L_number(base_name)
        train.append(base_name)

        annotations.append(process_zed_file(input_path, output_dir,label))
        
        data = {
                "split": {
                    "xtrain":train,
                    "xval":val,
                    "xtest":test},
                "annotations":annotations
                }


    with open(os.path.join(output_dir, 'annotation.pkl'), 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    batch_process(
            input_dir = 'zed_data',
            output_dir= 'pickle_data'
            )
    


















