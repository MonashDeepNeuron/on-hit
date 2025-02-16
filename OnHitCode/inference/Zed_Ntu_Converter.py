import numpy as np


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
    ntu_joints = 25

    keypoints = np.zeros((ntu_joints,3), dtype = np.float32)

    for index,kp in enumerate(body_data) :
        
        
        #this iterates through the zed points and maps it to the correct ntu joint location
        if kp == [None,None,None]:
            continue
        elif index in ZED34_TO_NTU_MAPPING:
            ntu_index = ZED34_TO_NTU_MAPPING[index] - 1
            keypoints[ntu_index] = kp 

    max_val = np.max(np.abs(keypoints))
    if max_val > 0:
        keypoints /= max_val

    return keypoints