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

from AirQuality import airQuality_
from Tempature import tempature_
from Humidity import humidity_

class Mqtt_Driver:
    
    def __init__(self):
    
        
        self.last_sent_airQuality = 0
        self.last_sent_tempature = 0
        self.last_sent_humidity = 0
        
        
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
        global airQuality
        self.client.publish("raspberry/airQuality", payload=str(airQuality_[0]), qos=0, retain=True)
        self.last_sent_airQuality = airQuality_[0]
        
    def send_tempature(self):
        
        self.client.publish("raspberry/tempature", payload=str(tempature_[0]), qos=0, retain=True)
        self.last_sent_tempature = tempature_[0]
        
    def send_humidity(self):
        
        self.client.publish("raspberry/humidity", payload=str(humidity_[0]), qos=0, retain=True)
        self.last_sent_humidity = humidity_[0]
        
    def send_data(self):
        
        
        t = 1
        
        sleep(1)
        
        while True:
            
            try:
                    
                if  abs(airQuality_[0] - self.last_sent_airQuality) >= 10:
                    self.send_airQuality()
                    sleep(t)
                
                if abs(tempature_[0] - self.last_sent_tempature) >= 1:
                    self.send_tempature()
                    sleep(t)
                
                if abs(humidity_[0] - self.last_sent_humidity) >= 1:
                    self.send_humidity()
                    sleep(t)
                    
                sleep(10)
                
                
            except BaseException as err:
                print(err)
                sleep(5)













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
    
    
