
import pyaudio
import wave
import os
import shutil
import time

class Recorder:

    def __init__(self):

        if not os.path.isdir("./Records"):
                os.mkdir("./Records")



        self.pa = pyaudio.PyAudio()

        self.stream_in = self.pa.open(
                                        rate=22050,
                                        channels=1,
                                        format=pyaudio.paInt16,
                                        input=True,                   # input stream flag
                                        input_device_index=7,         # input device index
                                        frames_per_buffer=1024
                                     )

    
    def save_audio(self, input_audio):

        if os.listdir("./Records").__len__() > 15:

            recorded_files = os.listdir("./Records")
            recorded_files.sort(reverse=True)

            for file in recorded_files[5:]:
                os.remove("./Records/"+file)
                

        output_filename = "./Records/" + time.strftime("%d%b%Y-%H.%M.%S", time.localtime()) + ".raw"


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
    input_audio = recorder.stream_in.read( 5 * 22050 )
    

    

    recorder.save_audio(input_audio)


    
    
    
