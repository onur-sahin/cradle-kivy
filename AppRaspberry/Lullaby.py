from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
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
from kivy.uix.popup import Popup


class LullabyWidget(BoxLayout):

    is_paused = False
    is_started = False

    always_repeat_current_music = BooleanProperty(False)
    random_play_music = BooleanProperty(False)
    repeat_playlist = BooleanProperty(True)
    lullaby_volume = NumericProperty(0.5)
    
    auto_play_status = BooleanProperty(False)


    music_directory = StringProperty("/")
    filePath = StringProperty("")

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

    def play(self):
        
        if(self.listofsongs.__len__() == 0):
            self.show_load()
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



    def replay(self):
        mixer.music.rewind()



    def next(self):

        self.stop()

        self.index += 1

        if(self.listofsongs.__len__() <= self.index):
            self.index = 0

        if(self.listofsongs.__len__() != 0):
            self.play()
            

    def back(self):

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


    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, path=self.music_directory)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.5, 0.5))
        self._popup.open()

    
    

    def load(self, path, filename):
        
        print(type(path))
        print(path)
        print(type(filename))
        print(filename)
        
        self.listofsongs.clear()

        selected_music = None
        
        
        if(os.path.isdir(filename[0])):
            self.music_directory = filename[0]
            
                
        else:
            self.music_directory = path
            selected_music = os.path.basename(filename[0])
            print(selected_music)
     

        # os.chdir(self.music_directory)

        counter = 0

        for file in os.listdir(self.music_directory):
            if file.endswith(".mp3"):
                print('file is ',file)
                songName = file.split('.')[0]
                print('songName is ',songName)
                self.realnames.append(songName)
                
                self.listofsongs.append(file)


            if str(file) == str(selected_music):
                self.index = self.listofsongs.__len__()-1

            print(self.index)

            counter += 1

        for file in self.realnames:
            self.formattedlist.append(file)
            #formattedlist.append(file + "\n")
            
        if self.is_started == True:
            self.stop()
            self.play()
            
    
                
                
            


    def on_touch_music_volume_slider(self, self_slider):
        self.lullaby_volume = self_slider.value
        mixer.music.set_volume(  float(self.lullaby_volume)/100  )
        pass
        
        
        
    
            
    def auto_play(self, btn_auto_play):
        if btn_auto_play.state == 'down':
            
            if(self.listofsongs.__len__() == 0):
                self.show_load()
            
            if(not self.parent.parent.ids.cradleGridLayout.listen_thread.is_alive()):
            
                self.parent.parent.ids.cradleGridLayout.listen_thread = threading.Thread(target=self.parent.parent.ids.cradleGridLayout.listen_baby,
                                                      args=(self.parent.parent.ids.cradleGridLayout.ids.auto_start_cradle,
                                                            self.parent.parent.ids.cradleGridLayout.ids.auto_stop_cradle,
                                                            self.parent.parent.ids.cradleGridLayout.ids.btn_cradle,
                                                            self.parent.parent.ids.cradleGridLayout.ids.btn_stop,
                                                            btn_auto_play)
                                                     )
                self.parent.parent.ids.cradleGridLayout.listen_thread.start()
            
                print("def on_press_btn_auto_stop(self, self_btn):")
            
        

class LoadDialog(FloatLayout):
    
    path = StringProperty("")

    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

   




    def directorychoose(self):
        
        # os.chdir(self.music_directory)

        for file in os.listdir(self.music_directory):
            if file.endswith(".mp3"):
                print('file is ',file)
                songName = file.split('.')[0]
                #print('songName is ',songName)
                self.realnames.append(songName)
                
                self.listofsongs.append(file)

        for file in self.realnames:
            self.formattedlist.append(file)



