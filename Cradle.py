
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from Motor_Control import Motor_Control
from __main__ import hallSensor
from time import sleep


class CradleGridLayout(GridLayout):

    motor_control = Motor_Control()

    def on_press_btn_cradle(self, speed, btn_cradle, btn_stop):
        
        btn_cradle.disabled = True
        self.motor_control.motor_start(speed)
        btn_stop.disabled = False
        
    def on_press_btn_stop(self, btn_cradle, btn_stop):
        
        btn_stop.disabled = True
        

        for i in range(0, 100001):

            if hallSensor.hallSensorState() == False:
                self.motor_control.motor_stop()
                break

            elif(i == 100000):
                self.motor_control.motor_stop()
            
            # sleep(0.0001)
        

        btn_cradle.disabled = False
                
            

    def on_touch_move_speed_slider(self, self_slider):
        self.motor_control.set_speed(self_slider.value)
        
        
    def on_press_btn_auto_start(self, self_btn):
        print("def on_press_btn_auto_start(self, self_btn):")
        
        
    def on_press_btn_auto_stop(self, self_btn):
        print("def on_press_btn_auto_stop(self, self_btn):")



