
import kivy
#kivy.require('1.11.1') # replace with your current kivy version !
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.camera import Camera
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.window import Window
import numpy as np
#from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission

class CameraApp(App):
    def build(self):


        if platform == "android":
            request_permissions([Permission.INTERNET,
                             Permission.CAMERA,
                             Permission.WRITE_EXTERNAL_STORAGE,
                             Permission.READ_EXTERNAL_STORAGE])

        self.snapshot = None
        self.root = Widget()
        self.width = Window.size[0]
        self.height = Window.size[1]

        # # CAMERA Works
        self.camera = Camera(resolution=(640, 480), size=(self.width, self.height), pos=(100, 100), state='play')

        # # IP CAMERA does NOT Work 
        # # Loads black screen
       #self.camera = Video(source="http://158.58.130.148:80/mjpg/video.mjpg", state='play')

        # # Video file does NOT Work 
        # self.camera = Video(source='/storage/emulated/0/Movies/MY-TEST-VIDEO.avi', state='play')

        Clock.schedule_interval(self.get_texture1, 1.0 / 25.0)
        return self.root


    def get_texture1(self, event):

        self.snapshot = self.camera.texture

        if self.snapshot != None:

            self.reg = self.snapshot.get_region(0, 0, 50, 50)

            # data processing here on numpy array
            nparr = np.fromstring(self.camera.texture.pixels, dtype=np.uint8)

            # # Just reshape
            # a = np.reshape(nparr, (480, 640, 4))
            
            # # Reshape, Flip, Rotate and make Copy of frame
            frame_reshaped = np.reshape(nparr, (480, 640, 4))
            frame_flipped = np.flip(frame_reshaped, axis=0)
            a = np.rot90(frame_flipped, 1)
            copy = np.copy(a)

            # # Draw on frame
            a[50:50+50, 50:50+50] = 255

            texture = Texture.create(size=(a.shape[1], a.shape[0]), colorfmt='rgba')
            texture.blit_buffer(a.tostring(), bufferfmt='ubyte', colorfmt="rgba")
            texture.flip_vertical()

            self.root.canvas.clear()

            with self.root.canvas:
                Rectangle(texture=texture, size=(a.shape[1], a.shape[0]), pos=(100, 100))


if __name__ == "__main__":
    CameraApp().run()
