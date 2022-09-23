
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

from Motor_Control import Motor_Control
from __main__ import hallSensor
from time import sleep
import time
import requests
from SoundSensor import SoundSensor
import threading
from Recorder import Recorder
from kivy.properties import DictProperty

from time import perf_counter

class CradleGridLayout(GridLayout):
    
    tic = perf_counter()
    toc = perf_counter()
    
    count_for_rocking = 0
    
    sleep_time = 10
    
    rocking_time = 0
    
    
    crying_status = False
    sound_status = False

    motor_control = Motor_Control()
    
    motor_speed = NumericProperty(25)
    
    soundSensor   = SoundSensor()
    
    listen_thread = threading.Thread()
    
    speed_thrd = threading.Thread()
    
    recorder = Recorder()
    
    
    cradle_auto_rocking_time = 30 # seconds
    
    herokuURL = "http://cradle-server.herokuapp.com/predict"
    
    
    resp = DictProperty()
    

    def on_press_btn_cradle(self, btn_cradle, btn_stop):
        
        btn_cradle.disabled = True
        self.start_cradle()
        btn_stop.disabled = False
        
    def start_cradle(self):
        self.motor_control.motor_start(self.motor_speed)
        
        
    def on_press_btn_stop(self, btn_cradle, btn_stop):
        
        btn_stop.disabled = True
        
        self.stop_cradle()

        btn_cradle.disabled = False
        
        
    def stop_cradle(self):
        
        toc = 0.0
        tic = time.perf_counter()
        
        while toc - tic < 5:
        
            for i in range(0, 1000000):
               
                if hallSensor.hallSensorState() == False:
                        
                    self.motor_control.motor_stop()
                    return

            toc = time.perf_counter()
        
        self.motor_control.motor_stop()
        
        
                
            

    def on_touch_move_speed_slider(self, self_slider):
        self.motor_speed = int(self_slider.value)
        self.motor_control.set_speed(self.motor_speed)
        
        
    def on_state_btn_auto_start(self, auto_start_cradle, auto_stop_cradle, btn_cradle, btn_stop):
        
        if(not self.listen_thread.is_alive()):
        
            self.listen_thread = threading.Thread(target=self.listen_baby,
                                                  args=(auto_start_cradle, 
                                                        auto_stop_cradle,
                                                        btn_cradle,
                                                        btn_stop) 
                                                 )
            
            self.listen_thread.start()
            print("def on_press_btn_auto_start(self, auto_start_cradle, auto_stop_cradle):")
        
        
        
        
        
    def on_state_btn_auto_stop(self, auto_start_cradle, auto_stop_cradle, btn_cradle, btn_stop):
        
        if(not self.listen_thread.is_alive()):
        
            self.listen_thread = threading.Thread(target=self.listen_baby,
                                                  args=(auto_start_cradle,
                                                        auto_stop_cradle,
                                                        btn_cradle,
                                                        btn_stop)
                                                 )
            self.listen_thread.start()
        
            print("def on_press_btn_auto_stop(self, self_btn):")
            

    def set_motor_speed(self):
        
        while self.listen_thread.is_alive():
            
            self.ids.slider_speeds.value =  75*pow(2.718, self.count_for_rocking)/(75+pow(2.718, self.count_for_rocking)) +25
                
            if self.crying_status == True:
            
                if self.count_for_rocking <= 10:
                    self.count_for_rocking += 1
                
            if self.crying_status == False:
                
                if self.count_for_rocking > 0:
                    self.count_for_rocking -= 1
                
            sleep(5)
            
            
        
        
        
    def listen_baby(self, auto_start_cradle, auto_stop_cradle, btn_cradle, btn_stop):
        
        
        
        while auto_start_cradle.state=='down' or auto_stop_cradle.state=='down':
        
            
            self.sound_status = self.check_sound()
            
            
            
            if self.sound_status == True:
                
                input_audio = self.recorder.stream_in.read(5*self.recorder.sample_rate)
                
                try:
                    self.resp = requests.post(   "http://cradle-server.herokuapp.com/predict",
                                            files=None,
                                            data=input_audio
                                        ).json()
                                    
                                    
                except BaseException as err:
                    
                    print("error in post process:"+str(err))
                    sleep(5)
                    continue
                
                if max(self.resp["output_detection"], key=self.resp["output_detection"].get) == 'Crying baby':
                    print("bura3")
                    self.crying_status = True
                    self.tic = perf_counter()
                    
                else:
                    self.crying_status = False
                    
                
                
            
            
            if( auto_start_cradle.state=='down' and auto_stop_cradle.state=="normal" ):
                
                print("bura4")
                if(self.crying_status == True and self.motor_control.motor_status==False):
                    btn_cradle.state="down"
                    btn_cradle.disabled = True
                    btn_stop.disabled = False
            
                    self.start_cradle()
                    
                    print("bura5")
                    
                    if not self.speed_thrd.is_alive():
                    
                        self.speed_thrd = threading.Thread(target=self.set_motor_speed)
                    
                    
                    
                    
            elif(auto_start_cradle.state=='normal' and auto_stop_cradle.state=="down" ):
                
                if(self.crying_status == False):
                    btn_stop.state = "down"
                    btn_stop.disabled=True
                    self.stop_cradle()
                    btn_stop.state = "normal"
                    
                    btn_cradle.state = "normal"
                    btn_cradle.disabled = False
                
            elif(auto_start_cradle.state=='down' and auto_stop_cradle.state=="down" ):
                
                if(self.crying_status == True):
                    btn_cradle.state="down"
                    btn_cradle.disabled = True
                    btn_stop.disabled = False
                    self.start_cradle()
                    
                elif(self.crying_status == False):
                    btn_stop.state = "down"
                    btn_stop.disabled=True
                    self.stop_cradle()
                    btn_stop.state = "normal"
                    
                    btn_cradle.state = "normal"
                    btn_cradle.disabled = False
                
            # else can't be "normal" and "normal"
            
           
            sleep(self.sleep_time)
            print("def listen_Baby while sonu 10 sn'lik bekleme başladı: ")
        
        
            
        
        
    def check_sound(self)->bool:

        count = 0
        toc = 0.0
        tic = time.perf_counter()
        
        while toc-tic < 5:
            
            for i in range(10000):
                count += self.soundSensor.soundSensorState()
                
            toc = time.perf_counter()
                
            if count >= 1000:
                return True
                
        print("listened=", toc-tic)
        return False
        
        

        
                      
                      
        
        
        

            
            
            
        
        
        



