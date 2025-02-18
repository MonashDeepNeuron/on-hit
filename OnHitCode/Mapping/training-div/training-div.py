import sys
from  zedtopkl import ZEDCamera

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
    
    def label_video_capture(self):
        """
        Opens an instance where we can record and label data from the ZedSDK camera capture
        """

        # Loads the camera and pose estimation from the ZedSDK
        self.configure_camera()
        self.open_camera()

        # Begins video capture 
        while True:

            frame = self.single_frame_inference()
            cv2.imshow("Zed", frame["frame"])

            
        

    def store_data(self, dataset_name: str="",
                          ): 
        """
        Stores the recorded data into a json file, if not json file makes a new one. 
        """
        pass 
    
    def configure_dataset(self, split: list[int]):
        """
        Divides the data based on the split and configures the dataset into the ST-GCN format. 
        """
        pass 

    def json_to_pkl(self): 
        """
        Converts the json dataset into a pkl dataset ready to be fed into the ST-GCN for training, 
        """
        pass 

train = TrainingDivision() 
train.label_video_capture()
train.store_data()

train.configure_dataset([70,20,10])
train.json_to_pkl()
