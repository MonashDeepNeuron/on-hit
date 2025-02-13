import cv2 
import mediapipe as mp 
import numpy as np 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose 


mp4_path = "/Users/natha/Desktop/on-hit/OnHitCode/Mapping/mp4topkl/TestVideo.mp4" # must use absolute path
cap = cv2.VideoCapture(mp4_path) # have to use 1 for index for Mac Camera

while cap.isOpened():

    ret, frame = cap.read()

    cv2.imshow("Mediapipe Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break 

cap.release()
cv2.destroyAllWindows()


