
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

from Motor_Control import Motor_Control
from __main__ import hallSensor

from time import sleep
from datetime import datetime
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
    
    sleep_time = 1
    
    rocking_time = 0
    
    btn_id = 0
    
    crying_status = False
    sound_status = False

    motor_control = Motor_Control()
    
    motor_speed = NumericProperty(25)
    
    listening_sensitivity = NumericProperty(75.0)
    
    
    soundSensor   = SoundSensor()
    
    listen_thread = threading.Thread()
    
    speed_thrd = threading.Thread()
    
    recorder = Recorder()
    

    
    
    cradle_auto_rocking_time = 30 # seconds
    
    herokuURL = "http://cradle-server.herokuapp.com/predict"
    
    
    resp = DictProperty({"baby_status":"The baby is calm."})
    
    input_list = [0,0,0]
    
    resp_list = [0,0,0]
    

    def on_press_btn_cradle(self, btn_cradle, btn_stop):
        
        btn_cradle.disabled = True
        self.start_cradle(self.motor_speed)
        btn_stop.disabled = False
        
    def start_cradle(self, speed):
        self.motor_control.motor_start(speed)
        
        
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
        self.motor_speed = self_slider.value
        if self.motor_control.motor_status == True:
            self.motor_control.set_speed(self.motor_speed)
        
        
    def on_state_btn_auto_start(self, auto_start_cradle, auto_stop_cradle, btn_cradle, btn_stop):
        
        if(not self.listen_thread.is_alive()):
        
            self.listen_thread = threading.Thread(target=self.listen_baby,
                                                  args=(auto_start_cradle, 
                                                        auto_stop_cradle,
                                                        btn_cradle,
                                                        btn_stop,
                                                        self.parent.parent.ids.lullabyWidget.ids.btn_auto_play) 
                                                 )
            
            self.listen_thread.start()
            print("def on_press_btn_auto_start(self, auto_start_cradle, auto_stop_cradle):")
        
        
        
        
        
    def on_state_btn_auto_stop(self, auto_start_cradle, auto_stop_cradle, btn_cradle, btn_stop):
        
        if(not self.listen_thread.is_alive()):
        
            self.listen_thread = threading.Thread(target=self.listen_baby,
                                                  args=(auto_start_cradle,
                                                        auto_stop_cradle,
                                                        btn_cradle,
                                                        btn_stop,
                                                        self.parent.parent.ids.lullabyWidget.ids.btn_auto_play)
                                                 )
            self.listen_thread.start()
        
            print("def on_press_btn_auto_stop(self, self_btn):")
            

    def set_motor_speed(self):
        
        print("set_motor_speed")
        
        while self.listen_thread.is_alive() and self.motor_control.motor_status:
            
            print("motor speed:", str(self.ids.slider_speed.value))
            self.motor_speed = int( 75*pow(2.718, self.count_for_rocking/20)/(75+pow(2.718, self.count_for_rocking/20)) +25)
                
            self.set_speed_general(self.motor_speed)
            
            if self.crying_status == True:
            
                if self.count_for_rocking <= 180:
                    self.count_for_rocking += 1
                
            if self.crying_status == False:
                
                if self.count_for_rocking > 0:
                    self.count_for_rocking -= 1
                
            sleep(2)
            
            
    def set_speed_general(self, speed):
        self.motor_speed = speed
        self.ids.slider_speed.value =  self.motor_speed
        self.motor_control.set_speed(self.motor_speed)
        
    
        
        
        
    def listen_baby(self, auto_start_cradle, auto_stop_cradle, btn_cradle, btn_stop, btn_auto_play):
        
    
        
        while auto_start_cradle.state=='down' or auto_stop_cradle.state=='down' or btn_auto_play.state == 'down':
            
            
    
            self.sound_status = self.check_sound()
            
            
            
            if self.sound_status == True:
                
                for i in range(3):
                
                    self.input_list[i] = self.recorder.stream_in.read(self.recorder.sample_rate*5, exception_on_overflow=False)
                
                
                index = 0
                retry = 0
                while index < 3:
                    
                    try:
                        
                        self.resp_list[index] = requests.post( herokuURL,
                                                               files=None,
                                                               data=self.input_list[index]
                                                             ).json()
                                            
                        self.recorder.save_audio(self.input_list[index])
                        print("bura3")
                        print(self.resp_list[index])
                        
                        index += 1
                        retry = 0
                                
                    except BaseException as err:
                        if retry == 5:
                            return
                        
                        retry += 1
                        
                        print("error in post process:"+str(err))
                        sleep(2)
                        
             
                        
                result = None
                for resp in self.resp_list:
                    
                    if max(resp["output_detection"], key=resp["output_detection"].get) == 'Crying baby':
                        
                        if(result == None):
                            result = resp
                        
                        else:
                            if resp["output_detection"]["Crying baby"] > result["output_detection"]["Crying baby"]:
                                result = resp
                        
                
                if result == None:
                    self.crying_status = False
                    self.update_MessageRV("The baby is calm")
                else:
                    
                    if(result["output_detection"]["Crying baby"]*100 >= self.listening_sensitivity):
                        self.crying_status = True
                        self.update_MessageRV(result)
                    else:
                        self.crying_status = False
                        self.update_MessageRV(result)
                    
                print("crying_status:"+str(self.crying_status))
                
            else:
                self.crying_status = False
                self.update_MessageRV("The baby is calm")
                
            
            
            if( auto_start_cradle.state=='down' and auto_stop_cradle.state=="normal" ):
                
                print("bura4")
                
                if(self.crying_status == True and self.motor_control.motor_status==False):
                    btn_cradle.state="down"
                    btn_cradle.disabled = True
                    btn_stop.disabled = False
                    self.set_speed_general(25)
                    self.start_cradle(self.motor_speed)
                    
                    
                    print("bura5")
                    
                    if not self.speed_thrd.is_alive():
                    
                        self.speed_thrd = threading.Thread(target=self.set_motor_speed)
                        self.speed_thrd.start()
                        
                        
                                
                    
                    
                    
            elif(auto_start_cradle.state=='normal' and auto_stop_cradle.state=="down" ):
                
                if(self.crying_status == False):
                    
                    if not self.speed_thrd.is_alive() and self.motor_control.motor_status:
                    
                        self.speed_thrd = threading.Thread(target=self.set_motor_speed)
                        self.speed_thrd.start()
                        
                    if self.motor_speed < 26:
                        
                        btn_stop.state = "down"
                        btn_stop.disabled=True
                        
                        self.stop_cradle()
                        
                        btn_stop.state = "normal"
                        
                        btn_cradle.state = "normal"
                        btn_cradle.disabled = False
                        
                        auto_stop_cradle.state = "normal"
                        break
                
            elif(auto_start_cradle.state=='down' and auto_stop_cradle.state=="down" ):
                
                if not self.speed_thrd.is_alive() and self.motor_control.motor_status:
                    
                    self.speed_thrd = threading.Thread(target=self.set_motor_speed)
                    self.speed_thrd.start()
                
                if(self.crying_status == True and not self.motor_control.motor_status):
                    btn_cradle.state="down"
                    btn_cradle.disabled = True
                    btn_stop.disabled = False
                    self.start_cradle(self.motor_speed)
                    
                    if not self.speed_thrd.is_alive():
                    
                        self.speed_thrd = threading.Thread(target=self.set_motor_speed)
                        self.speed_thrd.start()
                    
                elif(self.crying_status == False and self.motor_control.motor_status):
                    
                    
                    
                    if self.motor_speed < 26:

                        btn_stop.state = "down"
                        btn_stop.disabled=True

                        self.stop_cradle()

                        btn_stop.state = "normal"

                        btn_cradle.state = "normal"
                        btn_cradle.disabled = False
                
            # else can't be "normal" and "normal"
            
            
            if btn_auto_play.state == 'down':
                if self.crying_status == True:
  
                    
                    if(self.parent.parent.ids.lullabyWidget.is_started == False):
                        self.parent.parent.ids.lullabyWidget.play()
                        
                    if(self.parent.parent.ids.lullabyWidget.is_paused == True):
                        self.parent.parent.ids.lullabyWidget.play()
                        
            
            print("def listen_Baby while sonu 10 sn'lik bekleme başladı: ")
            
            sleep(self.sleep_time)
            
            

        
            
        
        
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
        
        
        
    def update_MessageRV(self, resp):
        
        data = self.parent.parent.ids.messageRV.data
        
        if resp == 'The baby is calm':
        
            if data.__len__() == 0:
                data.append({'id':self.btn_id, 'message':resp, 'text': datetime.now().strftime('%H:%M')+": "+resp, 'halign':"left" })
                self.btn_id += 1
                return
            
            if data[0]['message'] == resp:
                return
            
            if data.__len__() >= 5:
                data.pop()
             
            else:
                data.insert(0, {'id':self.btn_id, 'message':resp, 'text': datetime.now().strftime('%H:%M')+": "+resp, 'halign':"left" })
                self.btn_id += 1
        else:
            
            message = self.resp_to_str(resp["outputs_classification"])
            
            if data.__len__() == 0:
                data.append({'id':self.btn_id, 'message':message, 'text': datetime.now().strftime('%H:%M')+": "+message, 'halign':"left" })
                self.btn_id += 1
                return
            
            if data[0]['message'] == message:
                return
            
            if data.__len__() >= 5:
                data.pop()
             
            else:
                data.insert(0, {'id':self.btn_id, 'message':message, 'text': datetime.now().strftime('%H:%M')+": "+message, 'halign':"left"})
                self.btn_id += 1

  
    def resp_to_str(self, dct):
        
        text = ""
        
        for i in sorted(dct, key=dct.get, reverse=True):
            
            text += i + ": " + str(int(dct[i]*100)) + "%  " 
            
        return text
        
        
        
