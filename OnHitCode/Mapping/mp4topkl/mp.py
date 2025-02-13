import cv2 
import mediapipe as mp 
import numpy as np 

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose 


mp4_path = "/Users/natha/Desktop/on-hit/OnHitCode/Mapping/mp4topkl/TestVideo.mp4" # must use absolute path
cap = cv2.VideoCapture(1) # have to use 1 for index for Mac Camera

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()

        # recolour image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Recolour back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # print mediapipe results 
        print(results.pose_landmarks)

        cv2.imshow("Mediapipe Feed", image)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break 

    cap.release()
    cv2.destroyAllWindows()


