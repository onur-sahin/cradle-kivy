import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class CameraBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # camera = self.ids['camera']
        # timestr = time.strftime("%Y%m%d_%H%M%S")
        # camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

class DenemeApp(App):
  pass
  
if __name__ == "__main__":
    app = DenemeApp()
    app.run()
