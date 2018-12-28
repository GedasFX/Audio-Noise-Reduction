import sys
import wave
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as pyp

class WavFile:
    def __init__(self, sampleRate, channelCount, sampleWidth, params, data):
        self.sampleRate = sampleRate
        self.channelCount = channelCount
        self.sampleWidth = sampleWidth
        self.data = data
        self.params = params

def show_wave_n_spec(speech):
    spf = wave.open(speech,'r')
    f = WavFile(spf.getframerate(), spf.getnchannels(), spf.getsampwidth(), spf.getparams(), np.fromstring(spf.readframes(-1), 'Int16'))
    spf.close()

    # Perform initial FFT
    fftdat = np.fft.rfft(f.data)

    # Collect the x axis for the fourier transform. Results are0 padded and dimentions will not align
    xfreq = np.delete(np.fft.rfftfreq(fftdat.size, d=1/f.sampleRate), 0)

    pyp.subplot(411)
    pyp.plot(f.data)
    pyp.title('Wave from and spectrogram of %s' % sys.argv[1])

    pyp.subplot(412)
    
    #meanval = mean(abs(fftraw))
    meanval = 1e+7
    print('a')
    print(len(fftdat)/2)
    
    print('b')
    pyp.plot(xfreq, abs(fftdat[:len(fftdat)//2]))

    pyp.subplot(413)
    fftdat[abs(fftdat) < meanval] = 0
    pyp.plot(abs(fftdat[:len(fftdat)//2]))

    pyp.subplot(414)
    newdat = np.fft.irfft(fftdat)
    newdat = np.round(newdat).astype('int16')
    pyp.plot(newdat)

    spf = wave.open("rez.wav", 'w')
    spf.setparams(f.params)
    spf.writeframes(newdat)
    spf.close()

    pyp.show()

fil = sys.argv[1]
show_wave_n_spec(fil)