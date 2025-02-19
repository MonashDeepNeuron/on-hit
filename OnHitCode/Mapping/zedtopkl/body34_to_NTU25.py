import numpy as np
import re
import json 
import pickle
import os
from tqdm import tqdm
'''
A dictionary to map the zed joints to right index of the ntu joints

Dict {
    zed_index:ntu_index
}
'''
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

def convert_zed34_to_ntu(body_data:list) -> np.array:
    '''
    Function to convert the zed skeleton into a ntu skeleton

    Input: 
        body_data: List(List) = A list, and the index corresponds to the cordinates of a joint

    Output:
        keypoints: a np.array, with a shape of [joint_number,cordinates] 

    '''
    ntu_joints = 25
    keypoints = np.zeros((ntu_joints,3), dtype = np.float32)

    #Iterate throught the keypoints to map them
    for index,kp in enumerate(body_data) :        
        #if no cordinates, then pass
        if kp == [None,None,None]:
            continue
        elif index in ZED34_TO_NTU_MAPPING:
            ntu_index = ZED34_TO_NTU_MAPPING[index] - 1
            keypoints[ntu_index] = kp 

    #this is to normalise the cordinates (0-1), generally Neural Networks require normalised points
    max_val = np.max(np.abs(keypoints))
    if max_val > 0:
        keypoints /= max_val

    return keypoints

def strip_trailing_L_number(path:str) -> int:
    '''
    Fuction that takes in a name, and extracts the label number
    Input:
        path: str = basename of your file e.g scene10L20

    Output:
       return :int = label number e.g scene10L20 -> 20
    '''
    match = re.search(r'L(\d+)$', path)
    return int(match.group(1)) if match else None  # Convert to int

def process_zed_file(input_path:str, class_label:int=0):
    '''
    This takes in a json file and then converts it into the needed, format for annotations to be trained

    Input:
        input_path:str = path of the json file.
        class_label:int = action label

    Output:
        return Dict{
        'frame_dir':str base_name = the name of clip, e.g scene10L20
        'total_frames':int max_frames,
        'keypoint': np.ndarray: shape [M x T x V x C]) 
        M: number of persons; 
        T: number of frames (same as total_frames); 
        V: number of keypoints (25 for NTURGB+D 3D skeleton, 17 for CoCo, 18 for OpenPose, etc. ); 
        C: number of dimensions for keypoint coordinates (C=2 for 2D keypoint, C=3 for 3D keypoint).
        'label':int =  action label eg 20
        }
    '''
    #load zed data 
    with open(input_path) as f:
        raw_data = json.load(f)

    bodies = {}
     
    for frame in raw_data["pose_data"]:
        
        #bodies in the frame
        for t,body in  enumerate(frame):
            
            #hard coded to assume that their is only ever one person
            body_id = 0 
            bodies.setdefault(body_id, []).append(body)
    
    num_bodies = 1   
    max_frames = max(len(frames) for frames in bodies.values())
    num_joints = 25
    num_cords = 3 #3d skeleton
    # np array in size [M x T x V x C]
    skeleton_array = np.full((num_bodies,max_frames,num_joints,num_cords), np.nan, dtype=np.float32)

    #this converts the the zed sksleton into the ntu skeleton
    for body_id, frames in bodies.items():
        
        for t,frame in enumerate( frames):

            keypoints = convert_zed34_to_ntu(frame["keypoints"])
            #once the skeleton is converted, directly place it into the keypoints np.array
            skeleton_array[body_id,t] = keypoints 
    base_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"

    return {
    'frame_dir': base_name,
    'total_frames': max_frames,
    'keypoint':skeleton_array, 
    'label': class_label
    }

def batch_process(input_dir,output_dir):
    '''
    This looks into a directoy full of JSON clips and then takes all of them to compile into a .pkl file
    The needed format for the pkl file can be seen on the mmaction website
    https://mmaction2.readthedocs.io/en/latest/user_guides/prepare_dataset.html
    Input:
        input_dir: str = string of the path to the directory containing the json
        output_dir: str = string of the path to the directory containing the pickle file
    
    
    '''
    #Containers for the splits and annotations
    annotations = []
    train = []
    val = []
    test = []

    os.makedirs(output_dir,exist_ok=True)

    for counter,file_name in enumerate(tqdm(os.listdir(input_dir))):
        if not file_name.endswith('.json'):
            continue 

        input_path = os.path.join(input_dir, file_name)
        base_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"
        label = strip_trailing_L_number(base_name)
        
        #Right now this is hard coded, the splits are not even, this was done when we were testing with only 3 clips
        if counter == 0:
            train.append(base_name)
        elif counter == 1:
            val.append(base_name)
        else:
            test.append(base_name)


        annotations.append(process_zed_file(input_path, output_dir,label))
        
        data = {
                "split": {
                    "xtrain":train,
                    "xsub_val":val,
                    "xsub_test":test},
                "annotations":annotations
                }


    with open(os.path.join(output_dir, 'annotation.pkl'), 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    batch_process(
            input_dir = 'zed_data',
            output_dir= 'pickle_data'
            )
    


















