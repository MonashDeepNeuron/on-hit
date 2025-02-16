import cv2
import sys
import pyzed.sl as sl
import ogl_viewer.viewer as gl
import cv_viewer.tracking_viewer as cv_viewer
import numpy as np
import json
from datetime import datetime
import argparse

class ZEDCamera:
    def __init__(self, resolution="HD1080", svo_file="", ip_address=""):
        """
        Initialize the ZED Camera
        :param resolution: Camera resolution (HD2K, HD1080, HD720, etc.)
        :param svo_file: Path to an SVO file if replaying
        :param ip_address: IP address for streaming input
        """
        self.zed = sl.Camera()
        self.init_params = sl.InitParameters()
        self.configure_camera(resolution, svo_file, ip_address)
        self.data_list = []
        self.max_bodies = 0
        self.frame_count = 0
    
    def body_tracking_parameters(self):
        pass

    def configure_camera(self, svo_file: str,
                         ip_address: str,
                         resolution: str,
                         fps: int=60
                         ) -> str:
        
        """
        Configures the ZED camera with specified input parameters.

        Args:
            svo_file (str): Path to an SVO file for replaying pre-recorded data.
            ip_address (str): IP address for streaming input from a remote ZED camera.
            fps (int): Desired frames per second for camera operation.
            resolution (str): Camera resolution, options include 'HD2K', 'HD1200', 'HD1080', 'HD720', 'SVGA', or 'VGA'.
        
        Returns:
            str: Confirms what path ZEDCamera is using - svo or ip_address
        """

        # checking if the ip address and the svo_file has a path
        if svo_file:
            self.init_params.set_from_svo_file(svo_file)
            print(f"[ZEDCamera] Using SVO File input: {svo_file}")
        elif ip_address:
            self.init_params.set_from_stream(ip_address)
            print(f"[ZEDCamera] Using Stream input: {ip_address}")
        else:
            print("[ZEDCamera] Using live camera stream")

        # list of camera resolution for mapping 
        res_map = {
            "HD2K": sl.RESOLUTION.HD2K,
            "HD1200": sl.RESOLUTION.HD1200,
            "HD1080": sl.RESOLUTION.HD1080,
            "HD720": sl.RESOLUTION.HD720,
            "SVGA": sl.RESOLUTION.SVGA,
            "VGA": sl.RESOLUTION.VGA
        }

        # Looks for the resolution specific, if not then just uses the default 1080 
        self.init_params.camera_resolution = res_map.get(resolution, sl.RESOLUTION.HD1080)
        print(f"[ZEDCamera] Using Camera in resolution {resolution}")

        # Configures the camera according to the functions parameters
        self.init_params.camera_fps = fps
        self.init_params.coordinate_units = sl.UNIT.METER
        self.init_params.depth_mode = sl.DEPTH_MODE.ULTRA
        self.init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    def open_camera(self, 
                    inference_threshold: int=40
                    ) -> str:
        """ 
        Open the ZED Camera and configure the pose estimation model

        Input: 
            inference_threshold (int) = The minimum confidence score require to keep a detection

        Output: 
            str: Confirms that body tracking and camera has been enabled 
         
        """
        err = self.zed.open(self.init_params)

        if err != sl.ERROR_CODE.SUCCESS:
            print("[ZEDCamera] Failed to open camera.")
            exit(1)

        # Enable positional tracking (for object detection)
        tracking_params = sl.PositionalTrackingParameters()
        self.zed.enable_positional_tracking(tracking_params)

        self.body_param = sl.BodyTrackingParameters()

        # specifies the body tracking model and the skeleton format
        self.body_param.detection_model = sl.BODY_TRACKING_MODEL.HUMAN_BODY_FAST
        self.body_param.body_format = sl.BODY_FORMAT.BODY_34

        self.body_param.enable_tracking = True
        self.body_param.enable_body_fitting = False

        self.zed.enable_body_tracking(self.body_param)
        self.body_runtime_param = sl.BodyTrackingRuntimeParameters()
        self.body_runtime_param.detection_confidence_threshold = inference_threshold

        print("[ZEDCamera] Camera and body tracking enabled.")

    def process_frames(self):
        """ Capture frames and process body tracking """
        camera_info = self.zed.get_camera_information()
        display_resolution = sl.Resolution(
            min(camera_info.camera_configuration.resolution.width, 1280),
            min(camera_info.camera_configuration.resolution.height, 720)
        )
        image_scale = [display_resolution.width / camera_info.camera_configuration.resolution.width,
                       display_resolution.height / camera_info.camera_configuration.resolution.height]

        viewer = gl.GLViewer()
        viewer.init(camera_info.camera_configuration.calibration_parameters.left_cam,
                    self.body_param.enable_tracking, self.body_param.body_format)

        bodies = sl.Bodies()
        image = sl.Mat()
        key_wait = 10
        frame = 0 #frame counter
        return_dataset = [] 

        while viewer.is_available():
            if self.zed.grab() == sl.ERROR_CODE.SUCCESS:
                self.zed.retrieve_image(image, sl.VIEW.LEFT, sl.MEM.GPU, display_resolution) # must use GPU instead of CPU to take advantage of CUDA
                self.zed.retrieve_bodies(bodies, self.body_runtime_param)
                viewer.update_view(image, bodies)
                image_left_ocv = image.get_data()
                cv_viewer.render_2D(image_left_ocv, image_scale, bodies.body_list,
                                    self.body_param.enable_tracking, self.body_param.body_format)
                #the list of bodies within the frame
                if bodies.body_list:
                    for body in bodies.body_list:
                        #each body has unique attributes
                        body_data = {
                            "id": body.id,
                            "position": body.position.tolist(),
                            "keypoints": body.keypoint.tolist(), 
                            "frame":frame
                            }  
                        #this is the dataset that will be sent when the recording is done
                        return_dataset.append(body_data)           
               #increment the frame count 
                frame += 1
                cv2.imshow("ZED | 2D View", image_left_ocv)
                key = cv2.waitKey(key_wait)
                if key == ord('q'):  # Quit
                    print("[ZEDCamera] Exiting...")
                    viewer.exit()
                    self.cleanup()
                    #return the dataset 
                    return(return_dataset)
                    break
                elif key == ord('m'):  # Pause/Restart
                    key_wait = 0 if key_wait > 0 else 10
                    print("[ZEDCamera] Pause" if key_wait == 0 else "[ZEDCamera] Restart")


        viewer.exit()
        self.cleanup()

    def create_labeled_data(self, label, output_path="./zed_data/"):
        """ Save labeled pose data to JSON file """
        output_file = f"ann{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}L{label}.json"
        json_data = {
            "label": label,
            "pose_data": self.data_list,
            "bodies": self.max_bodies
        }
        with open(output_path + output_file, "w") as f:
            json.dump(json_data, f, indent=4)
        print(f"[ZEDCamera] Labeled data saved: {output_file}")

    def cleanup(self):
        """ Cleanup resources """
        self.zed.disable_body_tracking()
        self.zed.disable_positional_tracking()
        self.zed.close()
        cv2.destroyAllWindows()
        print("[ZEDCamera] Resources released.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_svo_file', type=str, default='', help='Path to an .svo file')
    parser.add_argument('--ip_address', type=str, default='', help='IP Address for streaming')
    parser.add_argument('--resolution', type=str, default='HD1080', help='Camera resolution')

    args = parser.parse_args()

    if args.input_svo_file and args.ip_address:
        print("Specify only input_svo_file or ip_address, not both. Exiting.")
        exit()

    zed_cam = ZEDCamera(resolution=args.resolution, svo_file=args.input_svo_file, ip_address=args.ip_address)
    zed_cam.open_camera()
    zed_cam.process_frames()
