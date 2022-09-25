import matplotlib.pyplot as plt
# import librosa
import soundfile


sig = soundfile.read("/home/pi/projects/cradle-kivy-geany/AppRaspberry/Records/2022Sep25-12.24.13.wav")

plt.plot(sig[0])

plt.show()
