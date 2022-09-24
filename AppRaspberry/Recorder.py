
import pyaudio
import wave
import os
import shutil
import time
import requests


from kivy.properties import DictProperty

class Recorder:
    
    sample_rate = 44100
    chuck_size = 4096
    last_audio_path = ""
    
    a = DictProperty({})
    

    def __init__(self):

        if not os.path.isdir("./Records"):
                os.mkdir("./Records")
                
      


        self.pa = pyaudio.PyAudio()
        
        # for i in range( self.pa.get_device_count() ) :
            # print("############################################################")
            # print(self.pa.get_device_info_by_index(i))
                                     
                    
        self.stream_in = self.pa.open(
                                        rate=self.sample_rate,
                                        channels=1,
                                        format=pyaudio.paInt16,
                                        input=True,                   # input stream flag
                                        input_device_index=2,         # input device index
                                        frames_per_buffer=self.chuck_size
                                     )

    
    def save_audio(self, input_audio):

        if os.listdir("./Records").__len__() > 15:

            recorded_files = os.listdir("./Records")
            recorded_files.sort(reverse=True)

            for file in recorded_files[5:]:
                os.remove("./Records/"+file)
                

        self.last_audio_path = "./Records/" + time.strftime("%Y%b%d-%H.%M.%S", time.localtime()) + ".wav"
        
        
        wav_file = wave.open(self.last_audio_path, 'wb')



        # define audio stream properties
        wav_file.setnchannels(1)        # number of channels  - mono channel
        wav_file.setsampwidth(2)        # sample width in bytes
        wav_file.setframerate(self.sample_rate)    # sampling rate in Hz
        
        

        # write samples to the file
        wav_file.writeframes(input_audio)
        
        wav_file.close()
        



if __name__ == "__main__":
    

    recorder = Recorder()
    
    # read 5 seconds of the input stream 
    tic = time.perf_counter()
    input_audio = recorder.stream_in.read( recorder.sample_rate*5 )
    toc = time.perf_counter()
    print(toc-tic)
    recorder.save_audio(input_audio)
    
    
    
    # input_audio = recorder.stream_in.read( recorder.sample_rate*5 )
    
    # recorder.save_audio(input_audio)
    
    
    # input_audio = recorder.stream_in.read( recorder.sample_rate*5 )
    
    # recorder.save_audio(input_audio)
        
    # resp = requests.post(   "http://cradle-server.herokuapp.com/predict",
                            # files=None,
                            # data=input_audio #bytes
                        # ).json()
    
    # print(resp["output_detection"])
    
    
    # recorder.a = requests.post(   "http://cradle-server.herokuapp.com/predict",
                            # files={"file":open(recorder.last_audio_path, "rb")},
                            # data=None
                        # )
    
    # print(recorder.a.text)
    
    
