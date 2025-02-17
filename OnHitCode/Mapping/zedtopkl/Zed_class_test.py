from Zed_class import *
import cv2


zed = ZEDCamera()
zed.configure_camera()
zed.open_camera()


while True:
    frame_data = zed.single_frame(True)

    print(frame_data)
    cv2.imshow("Zed",frame_data["frame"])
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("break")
        cv2.destroyAllWindows()
        zed.cleanup()
        break













