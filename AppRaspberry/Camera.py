from picamera import PiCamera
from time import sleep

class Camera:

    def __init__(self):
        self.camera = PiCamera()


    def takePhoto(self):
        self.camera.start_preview()
        sleep(2)
        self.camera.capture("test.jpg")


if __name__ == "__main__":

    camera = Camera()

    camera.takePhoto()