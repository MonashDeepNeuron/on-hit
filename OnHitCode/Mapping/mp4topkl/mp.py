import cv2
import mediapipe as mp 
import numpy as np 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


mode_path = "/home/labuser/OnHit/OnHitCode/Mapping/mp4topkl/pose_landmarker_heavy.task"
video_path = "/home/labuser/OnHit/OnHitCode/Mapping/mp4topkl/TestVideo.mp4"

cap = cv2.VideoCapture(video_path)
while cap.isOpened():

    ret, frame = cap.read()
    cv2.imshow("Hello!", frame)