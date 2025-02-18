import numpy as np
import pickle
import cv2
import time

# NTU 25-joint Skeleton Connection List
ntu_skeleton = [
    (0,1),
    (0,12),
    (0,16),
    (1,20),
    (2,3),
    (4,5),
    (5,6),
    (6,7),
    (7,21),
    (7,22),
    (8,9),
    (9,10),
    (10,11),
    (11,23),
    (11,24),
    (12,13),
    (13,14),
    (14,15),
    (16,17),
    (17,18),
    (18,19),
    (20,2),
    (20,4),
    (20,8)
]

def project_3d_to_2d(joints, img_size=500):
    """
    Projects 3D keypoints into 2D space using a simple perspective projection.

    Inputs:
    joints (np.ndarray): Shape [V, 3] - 3D keypoints (X, Y, Z)
    img_size (int): Output image size.

    Outputs:
    projected_joints (np.ndarray): Shape [V, 2] - 2D keypoints (X, Y)
    """
    focal_length = 1000  # Adjust for perspective effect
    cam_dist = 2.5  # Virtual camera distance

    # Apply simple perspective projection
    projected_joints = np.zeros((joints.shape[0], 2), dtype=np.int32)
    for i, (x, y, z) in enumerate(joints):
        z = max(z + cam_dist, 0.1)  # Prevent division by zero
        projected_x = int(img_size / 2 + (x * focal_length) / z)
        projected_y = int(img_size / 2 - (y * focal_length) / z)  # Flip Y for correct display
        projected_joints[i] = [projected_x, projected_y]
    
    return projected_joints

def visualize_skeleton_animation_3d(keypoints, fps=10):
    """
    Visualizes an animated NTU 25-joint skeleton in 3D using OpenCV.

    Inputs:
    keypoints (np.ndarray): Shape [M x T x V x 3] (Must be 3D: C=3)
    fps (int): Frames per second for the animation.
    """
    M, T, V, C = keypoints.shape  # Extract dimensions
    
    # Check if input is in 3D
    if C != 3:
        raise ValueError(f"Expected 3D keypoints (C=3), but got C={C}")

    # Select first person (M=1)
    person_keypoints = keypoints[0]  # Shape: [T, 25, 3]

    # Create OpenCV window
    cv2.namedWindow("NTU 3D Skeleton", cv2.WINDOW_AUTOSIZE)

    # Animation Loop (Iterates over frames T)
    for t in range(T):
        # Get keypoints for current frame
        joints_3d = person_keypoints[t]  # Shape: [25, 3]

        # Project 3D keypoints to 2D
        joints_2d = project_3d_to_2d(joints_3d)

        # Create a blank image (White background)
        img_size = 500  # Image size
        img = np.ones((img_size, img_size, 3), dtype=np.uint8) * 255  # White background

        # Draw skeleton connections
        for joint1, joint2 in ntu_skeleton:
            if joint1 < len(joints_2d) and joint2 < len(joints_2d):
                pt1, pt2 = tuple(joints_2d[joint1]), tuple(joints_2d[joint2])
                cv2.line(img, pt1, pt2, (0, 0, 255), 2)  # Red skeleton lines

        # Draw joints
        for x, y in joints_2d:
            cv2.circle(img, (x, y), 5, (255, 0, 0), -1)  # Blue joints

        # Show frame
        cv2.imshow("NTU 3D Skeleton", img)
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break  # Press 'q' to exit

    cv2.destroyAllWindows()

'''
with open(r"annotation.pkl", "rb") as f:
    data = pickle.load(f)
# Visualize Skeleton Animation
visualize_skeleton_animation_3d(data["annotations"][0]["keypoint"], fps=10)
'''