from picamzero import Camera
import time

cam = Camera()
time.sleep(2)

cam.record_video("vid_test.mp4", duration = 5)