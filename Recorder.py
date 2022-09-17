
import pyaudio
import wave
import os
import shutil
import time

class Recorder:

    def __init__(self):

        if not os.path.isdir("./Records"):
                os.mkdir("./Records")



    def recordAndSave(self, seconds=5, save=False):

        self.pa = pyaudio.PyAudio()

        self.stream_in = self.pa.open(
        rate=48000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,                   # input stream flag
        input_device_index=1,         # input device index
        frames_per_buffer=1024
        )



        # read 5 seconds of the input stream
        input_audio = self.stream_in.read(seconds * 48000)

        
        if save == True:

            if os.listdir("./Records").__len__() > 15:

                recorded_files = os.listdir("./Records")
                recorded_files.sort(reverse=True)

                for file in recorded_files[5:]:
                    os.remove("./Records/"+file)
                    
                # shutil.rmtree("./Records")
                # os.mkdir("./Records")

            output_filename = "./Records/" + time.strftime("%d%b%Y-%H.%M.%S", time.localtime()) + ".raw"

            
            wav_file = wave.open(output_filename, 'wb')



            # define audio stream properties
            wav_file.setnchannels(1)        # number of channels
            wav_file.setsampwidth(2)        # sample width in bytes
            wav_file.setframerate(48000)    # sampling rate in Hz

            # write samples to the file
            wav_file.writeframes(input_audio)
            wav_file.close()

            # self.stream_in.stop_stream()
            
            self.pa.terminate()


        return input_audio


if __name__ == "__main__":

    recorder = Recorder()

    recorder.recordAndSave(5, True)


    # while not recorder.stream_in.is_stopped():
    #     print("stopped?:", recorder.stream_in.is_stopped())

    # recorder.recordAndSave(5, True)


    # recorder.recordAndSave(2, True)
    # recorder.recordAndSave(2, True)
    # recorder.recordAndSave(2, True)
    # recorder.recordAndSave(2, True)
    # recorder.recordAndSave(2, True)
    # recorder.recordAndSave(2, True)
    
    
