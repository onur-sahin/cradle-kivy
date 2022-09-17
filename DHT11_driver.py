	
# pip3 install adafruit-circuitpython-dht
# sudo apt-get install libgpiod2


import time
import board
import adafruit_dht
import psutil




class DHT11_driver():



    def __init__(self):
        # We first check if a libgpiod process is running. If yes, we kill it!
        for proc in psutil.process_iter():
            if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
                proc.kill()

        self.sensor      = adafruit_dht.DHT11(board.D6)
        self.temp        = "waiting"
        self.humidity    = "waiting"

    def getTempAndHumidity(self):

        self.updateDHT11()

        return  self.temp, self.humidity


    def updateDHT11(self):

        count = 0

        while True:

            count += 1

            try:
                self.temp = self.sensor.temperature
                self.humidity = self.sensor.humidity
                
                break

            except RuntimeError as error:
                print(error.args[0])
                time.sleep(2.0)
                continue
            
            except Exception as error:
                self.sensor.exit()
                raise error

            else:
                if count == 10:
                    self.temp = "error"
            
            time.sleep(2.0)


if __name__ == "__main__":

    dht11 = DHT11_driver()

    while True:

        dht11.updateDHT11() 

        print("Temperature: {}*C   Humidity: {}% ".format(dht11.temp, dht11.humidity))

        
        time.sleep(2.0)
