# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
from time import sleep


class Motor_Control:

    in1 = 24
    in2 = 23
    en = 25
    temp1 = 1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

    default_speed = 25
    p = GPIO.PWM(en, 1000)


    def set_speed(self, x = default_speed):
        self.p.ChangeDutyCycle(x)

       
    def motor_start(self, speed = default_speed):

        self.p.start(25)

        self.set_speed(100)
        sleep(2)

        self.set_speed(speed)

        
        
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.LOW)
        

    def motor_stop(self):

        self.p.stop()

        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)