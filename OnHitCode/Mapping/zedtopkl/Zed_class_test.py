from Zed_class import *


zed = ZEDCamera()

zed.open_camera()
print(zed.process_frames())