
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from Motor_Control import Motor_Control
from __main__ import hallSensor


class CradleGridLayout(GridLayout):

    motor_control = Motor_Control()

    def on_press_btn_cradle(self, speed):
        self.motor_control.motor_start(speed)

    def on_press_btn_stop(self):

        for i in range(0, 100001):

            if hallSensor.hallSensorState() == False:
                self.motor_control.motor_stop()
                break

            elif(i == 100000):
                self.motor_control.motor_stop()

    def on_touch_move_speed_slider(self, self_slider):
        self.motor_control.set_speed(self_slider.value)



