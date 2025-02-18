import cv2 
from typing import List
from Zed_class import ZEDCamera
ZEDCamera()

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
  
    def label_video_capture(self):
        """
        Opens an instance where we can record and label data from the ZedSDK camera capture
        """
        
        detections = []

        # Loads the camera and pose estimation from the ZedSDK
        self.configure_camera()
        self.open_camera()

        # Begins video capture 
        while True:

            # runs inference on a single frame the video
            output = self.single_frame_inference(False)

            # gets the frames and the keypoints of the detectiosn dict
            frame = output["frame"]
            detections = output["keypoints"]
            
            #displays the frames that were recorded 
            cv2.imshow("Zed", frame)

            key = cv2.waitKey(1) & 0xFF
            
            if key == ord("c"):
                
                print("Video Captured")
                cv2.destroyAllWindows()

                break 

        print(detections[0]["keypoints"])

        label = int(input("Enter Action label:")) 
      

    def store_data(self, dataset_name: str="",
                          ): 
        """
        Stores the recorded data into a json file, if not json file makes a new one. 
        """
        pass 
  
    def configure_dataset(self, split: List[int]):
        """
        Divides the data based on the split and configures the dataset into the ST-GCN format. 
        """
        pass 

    def json_to_pkl(self): 
        """
        Converts the json dataset into a pkl dataset ready to be fed into the ST-GCN for training, 
        """
        pass 

training = TrainingDivision()
training.label_video_capture()

