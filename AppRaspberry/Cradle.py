
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty

from Motor_Control import Motor_Control
from __main__ import hallSensor
import json
from time import sleep
from datetime import datetime
import time
import requests
from SoundSensor import SoundSensor
import threading
from Recorder import Recorder
from kivy.properties import DictProperty

from time import perf_counter

from Mqtt_Driver import Mqtt_Driver






class CradleGridLayout(GridLayout):
    
    tic = perf_counter()
    toc = perf_counter()
    
    count_for_rocking = 0
    
    sleep_time = 1
    record_count = 2
    
    rocking_time = 0
    
    btn_id = 0
    
    crying_status = False
    sound_status = False

    motor_control = Motor_Control()
    
    motor_speed = NumericProperty(25.0)
    
    last_sent_motor_speed = 25
    
    listening_sensitivity = NumericProperty(75.0)
    
    
    soundSensor   = SoundSensor()
    
    listen_thread = threading.Thread()
    
    speed_thrd = threading.Thread()
    
    
    recorder = Recorder()
    
    cradle_auto_rocking_time = 30 # seconds
    
    herokuURL = "http://cradle-server.herokuapp.com/predict"
    
    
    resp = DictProperty({"baby_status":"The baby is calm."})
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.mqtt_driver = Mqtt_Driver()
        
        self.mqtt_sent_data_thrd = threading.Thread(target=self.mqtt_driver.send_data)

        self.mqtt_sent_data_thrd.start()
        
        
        self.mqtt_driver.client.subscribe("mobil/#", qos=0)
        
        self.mqtt_driver.client.message_callback_add("mobil/btn_cradle", self.on_press_btn_cradle)
        self.mqtt_driver.client.message_callback_add("mobil/btn_stop", self.on_press_btn_stop)
        
        self.mqtt_driver.client.message_callback_add("mobil/btn_play", self.btn_play)
        self.mqtt_driver.client.message_callback_add("mobil/btn_stop_music", self.btn_stop_music)
        self.mqtt_driver.client.message_callback_add("mobil/btn_replay", self.btn_replay)
        self.mqtt_driver.client.message_callback_add("mobil/btn_next", self.btn_next)
        self.mqtt_driver.client.message_callback_add("mobil/btn_back", self.btn_back)
        
        self.mqtt_driver.client.message_callback_add("mobil/btn_auto_play", self.btn_auto_play)
        self.mqtt_driver.client.message_callback_add("mobil/btn_auto_start", self.btn_auto_start)
        self.mqtt_driver.client.message_callback_add("mobil/btn_auto_stop", self.btn_auto_stop)
        
        self.mqtt_driver.client.message_callback_add("mobil/slider_speed", self.on_touch_move_speed_slider)
        self.mqtt_driver.client.message_callback_add("mobil/slider_volume", self.update_volume)
        
        self.mqtt_get_data_thrd = threading.Thread(target=self.mqtt_driver.client.loop_forever)
        self.mqtt_get_data_thrd.start()
        
    
        self.mqtt_driver.client.publish("raspberry/btn_auto_play_state", payload="normal", qos=0, retain=True)
        self.mqtt_driver.client.publish("raspberry/btn_auto_start_state", payload="normal", qos=0, retain=True)
        self.mqtt_driver.client.publish("raspberry/btn_auto_stop_state", payload="normal", qos=0, retain=True)
        self.mqtt_driver.client.publish("raspberry/slider_speed", payload=str(self.motor_speed), qos=0, retain=True)
    
    def update_volume(self, *args):
        self.parent.parent.ids.lullabyWidget.on_touch_music_volume_slider(*args)
    
    def btn_play(self, *args):
        self.parent.parent.ids.lullabyWidget.play()
        
    def btn_stop_music(self, *args):
        self.parent.parent.ids.lullabyWidget.stop()
        
    def btn_replay(self, *args):
        self.parent.parent.ids.lullabyWidget.replay()
        
    def btn_next(self, *args):
        self.parent.parent.ids.lullabyWidget.next()
    
    def btn_back(self, *args):
        self.parent.parent.ids.lullabyWidget.back()
        
    def btn_auto_play(self, *args):
        
        if args[2].payload.decode() == 'down':
        
            if self.parent.parent.ids.lullabyWidget.ids.btn_auto_play.state != 'down':
                
    
                result = self.parent.parent.ids.lullabyWidget.auto_play()
                
                if result == False:
                    self.parent.parent.ids.lullabyWidget.ids.btn_auto_play.state = 'normal'
                    self.mqtt_driver.client.publish("raspberry/btn_auto_play_state", payload="normal", qos=0, retain=True)
                    
                else:
                    
                    self.parent.parent.ids.lullabyWidget.ids.btn_auto_play.state = 'down'
                
                    self.mqtt_driver.client.publish("raspberry/btn_auto_play_state", payload="down", qos=0, retain=True)
        
        elif args[2].payload.decode() == 'normal':
        
            if self.parent.parent.ids.lullabyWidget.ids.btn_auto_play.state != 'normal':
                self.parent.parent.ids.lullabyWidget.ids.btn_auto_play.state = 'normal'
                
            
            self.mqtt_driver.client.publish("raspberry/btn_auto_play_state", payload="normal", qos=0, retain=True)
        
                
                
    def btn_auto_start(self, *args):
        
        
        if args[2].payload.decode() == 'down':
        
            if self.ids.auto_start_cradle.state != 'down':
                self.ids.auto_start_cradle.state = 'down'
                self.on_state_btn_auto_start()
            
            self.mqtt_driver.client.publish("raspberry/btn_auto_start_state", payload="down", qos=0, retain=True)
        
        elif args[2].payload.decode() == 'normal':
        
            if self.ids.auto_start_cradle.state != 'normal':
                self.ids.auto_start_cradle.state = 'normal'
                
            
            self.mqtt_driver.client.publish("raspberry/btn_auto_start_state", payload="normal", qos=0, retain=True)
        
        
    def btn_auto_stop(self, *args):
        
        if args[2].payload.decode() == 'down':
        
            if self.ids.auto_stop_cradle.state != 'down':
                self.ids.auto_stop_cradle.state = 'down'
                self.on_state_btn_auto_stop()
            
            self.mqtt_driver.client.publish("raspberry/btn_auto_stop_state", payload="down", qos=0, retain=True)
        
        elif args[2].payload.decode() == 'normal':
        
            if self.ids.auto_stop_cradle.state != 'normal':
                self.ids.auto_stop_cradle.state = 'normal'
                
            
            self.mqtt_driver.client.publish("raspberry/btn_auto_stop_state", payload="normal", qos=0, retain=True)

        
    
    

    

    def on_press_btn_cradle(self, *args):
        
        self.ids.btn_cradle.disabled = True
        self.start_cradle(self.motor_speed)
        self.ids.btn_stop.disabled = False
        
    def start_cradle(self, speed):
        self.motor_control.motor_start(speed)
        
        
    def on_press_btn_stop(self, *args):

        self.ids.btn_stop.disabled = True
        
        self.stop_cradle()
        
        self.ids.btn_cradle.disabled = False
        
        
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
        
        
                
            

    def on_touch_move_speed_slider(self, *args):
        
        if len(args) == 0:
            self.motor_speed = self.ids.slider_speed.value
            
            if abs(self.motor_speed - self.last_sent_motor_speed) > 5:
                
                self.mqtt_driver.client.publish("raspberry/slider_speed", payload=str(self.motor_speed), qos=0, retain=True)
                self.last_sent_motor_speed = self.motor_speed
        else:
            
            self.motor_speed = float(args[2].payload.decode())
            self.last_sent_motor_speed = self.motor_speed
            
            
        if self.motor_control.motor_status == True:
            self.motor_control.set_speed(self.motor_speed)
            
            
            
            
            
    def on_state_btn_auto_start(self):
        
        if(not self.listen_thread.is_alive()):
        
            self.listen_thread = threading.Thread(target=self.listen_baby,
                                                  args=(self.ids.auto_start_cradle, 
                                                        self.ids.auto_stop_cradle,
                                                        self.ids.btn_cradle,
                                                        self.ids.btn_stop,
                                                        self.parent.parent.ids.lullabyWidget.ids.btn_auto_play) 
                                                 )
            
            self.listen_thread.start()
            print("def on_press_btn_auto_start(self, auto_start_cradle, auto_stop_cradle):")
        
        
          
        self.mqtt_driver.client.publish("raspberry/btn_auto_start_state",
                                        payload=self.ids.auto_start_cradle.state,
                                        qos=0,
                                        retain=True)
        
        
        
        
    def on_state_btn_auto_stop(self):
        
        if(not self.listen_thread.is_alive()):
        
            self.listen_thread = threading.Thread(target=self.listen_baby,
                                                  args=(self.ids.auto_start_cradle,
                                                        self.ids.auto_stop_cradle,
                                                        self.ids.btn_cradle,
                                                        self.ids.btn_stop,
                                                        self.parent.parent.ids.lullabyWidget.ids.btn_auto_play)
                                                 )
            self.listen_thread.start()
        
        print("def on_press_btn_auto_stop(self, self_btn):")
            
        self.mqtt_driver.client.publish("raspberry/btn_auto_stop_state",
                                        payload=self.ids.auto_stop_cradle.state,
                                        qos=0,
                                        retain=True)
            

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
                
                input_list = []
                
                for i in range(self.record_count):
                
                    input_list.append(self.recorder.stream_in.read(self.recorder.sample_rate*5, exception_on_overflow=False))
                
                
                index = 0
                retry = 0
                resp_list = []
                
                while index < self.record_count:
                    
                    try:
                        
                        resp_list.append(requests.post( self.herokuURL,
                                                        files=None,
                                                        data=input_list[index]
                                                      ).json()
                                        )
                                            
                        self.recorder.save_audio(input_list[index])
                        
                        print(resp_list[index])
                        
                        index += 1
                        retry = 0
                                
                    except BaseException as err:
                        if retry == 5:
                            return
                        
                        retry += 1
                        
                        print("error in post process:"+str(err))
                        sleep(2)
                        
             
                        
                result = None
                for resp in resp_list:
                    
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
                        self.update_message_btn("BABY IS CRYING!..")
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
        
    def reset_msg_btn(self, message_btn):
        message_btn.text = "NO MESSAGE"
        message_btn.background_color = (1,1,1,1)
        
    def update_message_btn(self, resp):
        self.parent.parent.ids.message_btn.text = resp
        self.parent.parent.ids.message_btn.background_color = (0.8, 0, 0, 0.8)
        
    def update_MessageRV(self, resp):
        
        data = self.parent.parent.ids.messageRV.data
        
        if resp == 'The baby is calm':
            
            warning = { 'time':datetime.utcnow().strftime('%H:%M'), 'msg':'THE BABY IS CALM', 'sub_msg':resp }
        
            if data.__len__() == 0:                
               
                data.append({'id':self.btn_id, 'text':warning['time']+": "+warning['sub_msg'], 'halign':"left" })
                
                self.mqtt_driver.client.publish("raspberry/warning", payload=json.dumps(warning), qos=0, retain=True)
                
                self.btn_id += 1
                return
            
            else:
            
                if data.__len__() >= 10:
                    data.pop()
                    
                if data[0]['text'][7:] == resp:
                    data.pop(0)
                 
            
                data.insert(0, {'id':self.btn_id, 'text':warning['time']+": "+warning['sub_msg'], 'halign':"left" })
                self.mqtt_driver.client.publish("raspberry/warning", payload=json.dumps(warning), qos=0, retain=True)
                self.btn_id += 1
        else:
            
            warning = {'time'   : datetime.utcnow().strftime('%H:%M'),
                       'msg'    : 'THE BABY IS CRYING',
                       'sub_msg': self.resp_to_str(resp["outputs_classification"])
                      }
            
            if data.__len__() == 0:
                data.append({'id':self.btn_id, 'text': warning['time']+": "+warning['sub_msg'], 'halign':"left" })
                self.mqtt_driver.client.publish("raspberry/warning", payload=json.dumps(warning), qos=0, retain=True)
                self.btn_id += 1
                return
            
            else:
                if data.__len__() >= 10:
                    data.pop()
                    
                if data[0]['text'][7:] == warning['sub_msg']:
                    data.pop(0)
                    
                data.insert(0, {'id':self.btn_id, 'text': warning['time']+": "+warning['sub_msg'], 'halign':"left"})
                self.mqtt_driver.client.publish("raspberry/warning", payload=json.dumps(warning), qos=0, retain=True)
                self.btn_id += 1

  
    def resp_to_str(self, dct):
        
        text = ""
        
        for i in sorted(dct, key=dct.get, reverse=True):
            
            text += i + ": " + str(int(dct[i]*100)) + "%  " 
            
        return text
        
        
        
    
        
        
        
        
