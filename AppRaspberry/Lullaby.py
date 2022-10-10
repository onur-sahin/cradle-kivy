from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from pygame import mixer
import os
from kivy.properties import Clock
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import StringProperty
import threading
import os
from time import sleep
from kivy.uix.popup import Popup



class LullabyWidget(BoxLayout):

    is_paused = False
    is_started = False
    

    always_repeat_current_music = BooleanProperty(False)
    random_play_music = BooleanProperty(False)
    repeat_playlist = BooleanProperty(True)
    lullaby_volume = NumericProperty(50)
    last_sent_volume = 50
    
    auto_play_status = BooleanProperty(False)


    music_directory = StringProperty("")
    filePath = StringProperty("")
    last_directory = "/home/pi/Desktop/"

    listofsongs = ListProperty([])
    formattedlist = ListProperty([])
    realnames = ListProperty([])
    index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mixer.init()

    def check_music(self, dt):

        if(self.is_started == True):

            if(mixer.music.get_busy() == False and self.is_paused == False):
                
                if(self.always_repeat_current_music == True):
                    pass
                elif(self.random_play_music == True):
                    pass
                elif(self.repeat_playlist == True):
                    self.next()

        else:
            pass
            
    def update_musics(self):

        if not os.path.isfile("./music_path.txt"):
            return False
            
        else:
            
            file = open("./music_path.txt", 'r')
            
            path = file.readline()
            
            file.close()
            
            if os.path.isfile(path):
                self.load(os.path.dirname(path), [path])
            else:
                self.load(path, [])
                
                
            return True
                

    def play(self):
    
        if(self.listofsongs.__len__() == 0):
            if not  self.update_musics():
                self.show_load()
                
                
        if(self.listofsongs.__len__() == 0):
            return
                
            
        
            
    
        if( self.is_paused == False and self.is_started == False):
    
            music = open(self.music_directory+'/'+self.listofsongs[self.index])

            mixer.music.load(music)
            mixer.music.set_volume(1)
            mixer.music.play()
            
            self.is_started = True

            Clock.schedule_interval(self.check_music, 1)

            

            

        elif(self.is_paused == True):
            mixer.music.unpause()
            self.is_paused = False

        elif(self.is_started == True and self.is_paused == False):
            mixer.music.pause()
            self.is_paused = True


    def stop(self):
        mixer.music.stop()
      
        self.is_started = False
        self.is_paused = False



    def replay(self, *args):
        mixer.music.rewind()



    def next(self, *args):

        self.stop()

        self.index += 1

        if(self.listofsongs.__len__() <= self.index):
            self.index = 0

        if(self.listofsongs.__len__() != 0):
            self.play()
            

    def back(self, *args):

        if(self.listofsongs.__len__() == 0):
            return

        self.stop()

        self.index -= 1

        if(self.listofsongs.__len__() <= self.index):
            self.index = 0

        if(self.index < 0):
            self.index = self.listofsongs.__len__()-1

        
        self.play()



    def dismiss_popup(self):
        
        self._popup.dismiss()
        self.popup_wait_flag = True
        
        
        

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, path=self.last_directory)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.5, 0.5))
        self._popup.open()
        
        

    
    

    def load(self, path, filename):
        
        
        self.listofsongs.clear()

        selected_music = None
        
        if filename.__len__() != 0:
        
            if(os.path.isdir(filename[0])):
                self.music_directory = filename[0]
                
                
                    
            else:
                self.music_directory = path
                selected_music = os.path.basename(filename[0])
                
        else:
    
            self.music_directory = path
            
            
        file = open("./music_path.txt", "w")
        file.write(self.music_directory)
        file.close()
     

        counter = 0

        for file in os.listdir(self.music_directory):
            if file.endswith(".mp3"):

                songName = file.split('.')[0]

                self.realnames.append(songName)
                
                self.listofsongs.append(file)


            if str(file) == str(selected_music):
                self.index = self.listofsongs.__len__()-1


            counter += 1

        for file in self.realnames:
            self.formattedlist.append(file)
            #formattedlist.append(file + "\n")
            
        if self.listofsongs.__len__() == 0:
            self.showPopup(title="Failure", text="There Is No Music!")
            return False
            
        if self.is_started == True:
            self.stop()
            self.play()
            
    
            
            
    
    def showPopup(self, title="No Title", text="No Text"):
          
        layout = GridLayout(cols = 1, padding = 10)
  
        popupLabel = Label(text = text)
        closeButton = Button(text = "OK")
  
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
  
        # Instantiate the modal popup and display
        popup = Popup(title = title,
                      content = layout,
                      size_hint =(None, None), size =(200, 200))  
        popup.open()   
  
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)              



            


    def on_touch_music_volume_slider(self, *args):
        
        if len(args) == 0:
            self.lullaby_volume = self.ids.slider_sound.value
            
            if abs(self.lullaby_volume - self.last_sent_volume) > 5:
                
                self.parent.parent.ids.cradleGridLayout.mqtt_driver.client.publish("raspberry/slider_volume",
                                                                                   payload=str(self.lullaby_volume),
                                                                                   qos=0,
                                                                                   retain=True)
                self.last_sent_volume = self.lullaby_volume
        else:            
            self.lullaby_volume = float(args[2].payload.decode())
            self.last_sent_volume = self.lullaby_volume
            
    
        mixer.music.set_volume(  float(self.lullaby_volume)/100  )
        
    
        

            
    def auto_play(self):
        
        if self.ids.btn_auto_play.state == 'down':
            
            if(self.listofsongs.__len__() == 0):
                
                if not  self.update_musics():
                    self.ids.btn_auto_play.state ='normal'
                    self.show_load()
                    return
                
                    
            if(self.listofsongs.__len__() == 0):
                self.ids.btn_auto_play.state = 'normal'
                return False
            
            if(not self.parent.parent.ids.cradleGridLayout.listen_thread.is_alive()):
            
                self.parent.parent.ids.cradleGridLayout.listen_thread = threading.Thread(target=self.parent.parent.ids.cradleGridLayout.listen_baby,
                                                      args=(self.parent.parent.ids.cradleGridLayout.ids.auto_start_cradle,
                                                            self.parent.parent.ids.cradleGridLayout.ids.auto_stop_cradle,
                                                            self.parent.parent.ids.cradleGridLayout.ids.btn_cradle,
                                                            self.parent.parent.ids.cradleGridLayout.ids.btn_stop,
                                                            self.ids.btn_auto_play)
                                                     )
                self.parent.parent.ids.cradleGridLayout.listen_thread.start()
            
                print("def on_press_btn_auto_stop(self, self_btn):")
                
        self.parent.parent.ids.cradleGridLayout.mqtt_driver.client.publish("raspberry/btn_auto_play_state",
                                                                           payload=self.ids.btn_auto_play.state,
                                                                           qos=0,
                                                                           retain=True)
            
        

class LoadDialog(FloatLayout):
    
    path = StringProperty("")

    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

   




    def directorychoose(self):
        
        # os.chdir(self.music_directory)

        for file in os.listdir(self.music_directory):
            if file.endswith(".mp3"):

                songName = file.split('.')[0]
                self.realnames.append(songName)
                self.listofsongs.append(file)

        for file in self.realnames:
            self.formattedlist.append(file)



