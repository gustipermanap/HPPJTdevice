from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.resolution = (200, 200)
camera.start_preview()
sleep(5)
camera.stop_preview()
