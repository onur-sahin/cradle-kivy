
import pyaudio
import wave
import os
import shutil
import time
import requests

class Recorder:
    
    sample_rate = 22050
    chuck_size = 1024

    def __init__(self):

        if not os.path.isdir("./Records"):
                os.mkdir("./Records")


        self.pa = pyaudio.PyAudio()

        self.stream_in = self.pa.open(
                                        rate=self.sample_rate,
                                        channels=1,
                                        format=pyaudio.paInt16,
                                        input=True,                   # input stream flag
                                        input_device_index=7,         # input device index
                                        frames_per_buffer=self.chuck_size
                                     )

    
    def save_audio(self, input_audio):

        if os.listdir("./Records").__len__() > 15:

            recorded_files = os.listdir("./Records")
            recorded_files.sort(reverse=True)

            for file in recorded_files[5:]:
                os.remove("./Records/"+file)
                

        output_filename = "./Records/" + time.strftime("%Y%b%d-%H.%M.%S", time.localtime()) + ".raw"


        wav_file = wave.open(output_filename, 'wb')



        # define audio stream properties
        wav_file.setnchannels(1)        # number of channels  - mono channel
        wav_file.setsampwidth(2)        # sample width in bytes
        wav_file.setframerate(22050)    # sampling rate in Hz
        
        

        # write samples to the file
        wav_file.writeframes(input_audio)
        wav_file.close()



if __name__ == "__main__":
    

    recorder = Recorder()
    
    # read 5 seconds of the input stream 
    input_audio = recorder.stream_in.read( 1024 )
    
    print(len(input_audio))
    byte_content = input_audio
    
    list_16bits = [byte_content[i + 1] << 8 | byte_content[i] for i in range(0, len(byte_content), 2)]
    print(list_16bits)
    
    for i, y in enumerate(input_audio):
        print(i, y)
    
    
    # print(input_a

    # recorder.save_audio(input_audio)
    
    
    # resp = requests.post("http://cradle-server.herokuapp.com/predict",
                      # files={"file":input_audio})


# resp = requests.post("http://localhost:5000/predict",
#                       files={"file":open("test.wav", "rb")})

    # print(resp.text)
    
    
