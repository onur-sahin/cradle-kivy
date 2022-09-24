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

    default_speed = 25.0
    current_speed = 0.0
    motor_status = False
    
    p = GPIO.PWM(en, 1000)


    def set_speed(self, x):
        
        if(self.current_speed != x):
            self.p.ChangeDutyCycle(x)
            current_speed = x

       
    def motor_start(self, speed):
        
        
        if self.motor_status == False:
        
            self.motor_status = True
                
            self.p.start(100.0)
            self.current_speed = 100
            
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            
            sleep(2)

            self.set_speed(speed)
        
        
        

    def motor_stop(self):
        
        if self.motor_status == True:
            
            self.motor_status = False
            
            self.p.stop()

            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
            
            
            
            
            
