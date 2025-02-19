from body34_to_NTU25 import * 
import time
import cv2 
from typing import List
from Zed_class import ZEDCamera
import random
import json 
import numpy as np 
import pickle as pkl  

"""

Training: 70
Validation: 20
Test: 10 

1) Capture video stream and label 
2) if existing datatset: 
        edit dataset for training instances
    else: 
        make new json file and write json 
3) dataset split [70,20,10] etc. 
4) Convert from json to pkl file 
"""

class TrainingDivision(ZEDCamera):

    def __init__(self):
        super().__init__()

    def write_STGCN_format(keypoints: dict):
        pass 
  
    def label_video_capture(self, clip_name: str,output_path:str):
        """
        Opens an instance where we can record and label data from the ZedSDK camera capture
        """
        #list to store frames within the clip
        detections = []

        # Loads the camera and pose estimation from the ZedSDK
        self.configure_camera()
        self.open_camera()
        key_wait = 10
        total_frames =  0 
        started = False
        # Begins video capture 
        while True:

            # runs inference on a single frame the video
            output = self.single_frame_inference(False)

            # increment the frame count 
            total_frames += 1

            # gets the frames and the keypoints of the detectiosn dict
            frame = output["frame"]
            
            detections.append( output["keypoints"])
            #displays the frames that were recorded 
            cv2.imshow("Zed", frame)

            key = cv2.waitKey(key_wait) & 0xFF
             
            if key == ord("c") and started:
                if (key_wait>0):
                    print("pause")
                    key_wait = 0
                    label = int(input("Enter Action label:")) 
                    json_data = {
                            "label": label,
                            "pose_data":detections}
                    
                    unix_time =str( int(time.time()))
                    with open(output_path + clip_name +unix_time + "L" + str(label)+ ".json","w") as f:
                        json.dump(json_data,f, indent = 4)
                    detections = []
                    started = False
                    print("stopped recording")
                    key_wait  =10

            elif key == ord("q"):
                print("exit")
                cv2.destroyAllWindows()
                self.cleanup()
                break
            elif key == ord('s'):  # Start
                if not started:
                    started = True
                    key_wait = 10  # Resume frame processing
                    print("[ZEDCamera] Started")
  
    def configure_dataset(self, split: List[float],input_dir:str,output_dir:str):
        """
        Divides the data based on the split and configures the dataset into the ST-GCN format. 
        """
        #Containers for the splits and annotations
        annotations = []
        train = []
        val = []
        test = []
        filenames = os.listdir(input_dir)
        random.shuffle(filenames)
        print(filenames)
        train_percent, val_percent,test_percent = split
        n = len(filenames)

        #this shuffles the filenames in the list so it is randomised
        #then go through each file name, pull the json and turn it into the correct format
        for counter,file_name in enumerate(tqdm(filenames)):
            if not file_name.endswith('.json'):
                continue 

            input_path = os.path.join(input_dir, file_name)
            clip_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"
            label = strip_trailing_L_number(clip_name)


            annotations.append(process_zed_file(input_path,label))
        
        #this will added the names into the catogories
        for _ in range(int(n*train_percent)):

            input_path = os.path.join(input_dir, filenames.pop(0))
            clip_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"
            train.append(clip_name)
        for _ in range(int(n*val_percent)):

            input_path = os.path.join(input_dir, filenames.pop(0))
            clip_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"
            val.append(clip_name)
        while len(filenames)>0:

            input_path = os.path.join(input_dir, filenames.pop(0))
            clip_name = f"{os.path.splitext(os.path.basename(input_path))[0]}"
            test.append(clip_name)


        data = {
                "split": {
                    "xtrain":train,
                    "xsub_val":val,
                    "xsub_test":test},
                "annotations":annotations
                }


        with open(os.path.join(output_dir, 'annotation.pkl'), 'wb') as f:
            pickle.dump(data, f)


training = TrainingDivision()
#training.label_video_capture("a","./json_clips/")
training.configure_dataset([0.7,0.2,0.1],"./json_clips/","./test_pkl_files")
