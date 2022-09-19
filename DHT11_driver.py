	
# pip3 install adafruit-circuitpython-dht
# sudo apt-get install libgpiod2


from time import sleep
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
        self.temp        = 0
        self.humidity    = 0

    def getTempAndHumidity(self):

        self.updateDHT11()

        return  self.temp, self.humidity


    def updateDHT11(self):


        while True:


            try:
                sleep(0.0001)
                self.temp = int( self.sensor.temperature )
                sleep(0.0001)
                self.humidity = int( self.sensor.humidity )
                sleep(0.0001)
                
                break
                
            except:
                pass

            # except RuntimeError as error:
                # sleep(0.0001)
                # print(error.args[0])
                # sleep(2.0)
                # continue
            
            # except BaseException as error:
                # sleep(0.0001)
                # self.sensor.exit()
                # raise error
            
        


if __name__ == "__main__":

    dht11 = DHT11_driver()

    while True:

        dht11.updateDHT11() 

        print("Temperature: {}*C   Humidity: {}% ".format(dht11.temp, dht11.humidity))

        
        sleep(2.0)
