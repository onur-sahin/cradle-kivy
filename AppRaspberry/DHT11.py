	
# pip3 install adafruit-circuitpython-dht
# sudo apt-get install libgpiod2


from time import sleep
import board
import adafruit_dht
import psutil




class DHT11():



    def __init__(self):
        
        # We first check if a libgpiod process is running. If yes, we kill it!
        for proc in psutil.process_iter():
            if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
                proc.kill()

        self.sensor      = adafruit_dht.DHT11(board.D6)

    def getTempAndHumidity(self):
        
        while True:
            
            try:
                return  int(self.sensor.temperature), int(self.sensor.humidity)

            except:
                pass
                
            sleep(0.001)
        


if __name__ == "__main__":

    dht11_driver = DHT11()

    while True:


        print("Temperature: {}*C   Humidity: {}% ".format(*dht11_driver.getTempAndHumidity()) )

        
        sleep(2.0)
