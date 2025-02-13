import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Load an image
image_path = "/Users/natha/Desktop/on-hit/OnHitCode/Mapping/mp4topkl/running.jpg"
image = cv2.imread(image_path)

# Convert image to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize Pose model
with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
    results = pose.process(image_rgb)  # Get pose landmarks

    if results.pose_landmarks:
        print("Detected Landmarks:")
        for i, landmark in enumerate(results.pose_landmarks.landmark):
            print(f"Landmark {i}: x={landmark.x}, y={landmark.y}, z={landmark.z}, visibility={landmark.visibility}")

        # Draw landmarks on the image
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Show the image with landmarks
        cv2.imshow("Pose Landmarks", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No landmarks detected.")
