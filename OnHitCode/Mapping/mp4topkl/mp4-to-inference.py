import cv2 
import mediapipe as mp 
import numpy as np 

class mp4_to_mediapipe():

    MP_POSE = mp.solutions.pose 
    
    def __init__(self, video_path: str):
        self.video_path = video_path
    
    def mediapipe_inference(self, min_detection_threshold: int, min_tracking_threshold: int) -> str:
        """
        Returns a nested dictionary which has the 33 landmarks - each landmark corresponds to its own dictionary
        this dictionary has the x,y,z coordinates and their visibility 
        """

        cap = cv2.VideoCapture(self.video_path)
        MP_POSE = mp.solutions.pose 


        with MP_POSE.Pose(min_detection_confidence=min_detection_threshold, min_tracking_confidence=min_tracking_threshold) as pose: 

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    print("Completed")
                    break 

                # recolour image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolour back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # print mediapipe results 
                print(results.pose_landmarks) # dictionary with index as the landmarks (0-32), has a nested dictionary with x,y,x and confidence

            cap.release()




mp4_path = "/Users/natha/Desktop/on-hit/OnHitCode/Mapping/mp4topkl/TestVideo.mp4" 
video = mp4_to_mediapipe(mp4_path)
video.mediapipe_inference(0.5, 0.5)
