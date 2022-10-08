#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import time
import paho.mqtt.client as paho
from paho import mqtt
import threading
from time import sleep
from datetime import datetime, timedelta


# from AirQuality import airQuality_
# from Tempature import tempature_
# from Humidity import humidity_

class Mqtt_Driver:
    
    def __init__(self, lm35_driver, mq135_driver, dht11_driver, flameSensor):
        
        self.delta = timedelta(minutes=3)
        
        self.lm35_driver  = lm35_driver
        self.mq135_driver = mq135_driver
        self.dht11_driver = dht11_driver
        self.flameSensor  = flameSensor
        
        self.airQuality          = 0
        self.temperature         = 0
        self.humidity            = 0
        self.flame_status        = False
        self.time_flameDetection = datetime.fromisoformat('2000-00-00 00:00:00.000')
        
        self.last_sent_airQuality          = -100
        self.last_sent_temperature         = -273
        self.last_sent_humidity            = -100
        self.last_sent_time_flameDetection = datetime.fromisoformat('2000-00-00 00:00:00.000')
        
        
        # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
        # userdata is user defined data of any type, updated by user_data_set()
        # client_id is the given name of the client
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set("ahmedmehmed", "235711Int1")
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect("e78f75ef51644ecda4a26c0c6d5f9b13.s1.eu.hivemq.cloud", 8883)

        # setting callbacks, use separate functions like above for better visibility
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        
        
        
    
   

    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


    
    def send_airQuality(self):
        
        try:
            self.client.publish("raspberry/airQuality", payload=str(self.airQuality), qos=0, retain=True)
            self.last_sent_airQuality = self.airQuality
        
        except BaseException as err:
            print(err)
            sleep(1)
        
    def send_temperature(self):
        
        try:
            self.client.publish("raspberry/tempature", payload=str(self.temperature), qos=0, retain=True)
            self.last_sent_temperature = self.temperature
            
        except BaseException as err:
            print(err)
            sleep(1)
            
    def send_humidity(self):
        
        try:
            self.client.publish("raspberry/humidity", payload=str(self.humidity), qos=0, retain=True)
            self.last_sent_humidity = self.humidity
            
        except BaseException as err:
            print(err)
            sleep(1)
            
            
    def send_flameDetected(self):
        
        try:
            self.client.publish("raspberry/flameDetected", payload=self.time_flameDetection.strftime('%H:%M'), qos=0, retain=True)
            
        except BaseException as err:
            print(err)
            sleep(1)
        
        
    def send_data(self):
        
        t = 2
        
        while True:
            
                
                self.airQuality = self.mq135_driver.getAirQuality()
        
                if abs(self.airQuality - self.last_sent_airQuality) >= 10:
                    self.send_airQuality()
                    
                
                self.temperature = self.lm35_driver.getTemperature()
                
                if abs(self.temperature - self.last_sent_temperature) >= 1:
                    self.send_temperature()
                    
                
                _, self.humidity = self.dht11_driver.getTempAndHumidity()

                if abs(self.humidity - self.last_sent_humidity) >= 5:
                    self.send_humidity()
                    
                    
                sleep(t)
                
                
    def check_sensors(self):
        
        t = 0.5
        
        while True:
            
            self.flame_status = self.flameSensor.getFlameSensorState()
            
            
            if self.flame_status == True:
                
                if self.time_flameDetection - self.last_sent_time_flameDetection > self.delta:
                    
                    self.time_flameDetection = datetime.utcnow()
                    self.send_flameDetected()
                    
            sleep(t)


if __name__=="__main__":

    mqtt_driver = Mqtt_Driver()


    # subscribe to all topics of encyclopedia by using the wildcard "#"
    mqtt_driver.client.subscribe("testtopic/#", qos=0)

    # a single publish, this can also be done in loops, etc.
    mqtt_driver.client.publish("testtopic", payload="deneme125", qos=0)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    # mqtt_driver.client.loop_start()

    mqtt_driver.client.loop_forever()
    
    
