import sys
import wave
import numpy as np
import matplotlib.pyplot as pyp

class WavFile:
    def __init__(self, sampleRate, channelCount, sampleWidth, params, data):
        self.sampleRate = sampleRate
        self.channelCount = channelCount
        self.sampleWidth = sampleWidth
        self.data = data
        self.params = params

def readInitialAudio(path):
    spf = wave.open(path)
    print('Started reading file ' + path)
    f = WavFile(spf.getframerate(), spf.getnchannels(), spf.getsampwidth(), spf.getparams(), np.fromstring(spf.readframes(-1), 'Int16'))
    spf.close()
    print('Finished reading file.')
    return f

if __name__ == "__main__":
    # Read initial waveform audio file
    f = readInitialAudio(sys.argv[1])

    # Perform initial real FFT
    print('Started FFT')
    fftdat = np.fft.rfft(f.data)

    # Generate the x axis for the fourier transform. Results are 0 padded and dimentions will not align, need to remove the padding
    xfreq = np.delete(np.fft.rfftfreq(fftdat.size, d=1/f.sampleRate), 0)

    pyp.figure(figsize=(10,8))
    #pyp.title('Wave from of %s' % sys.argv[1])

    print('Plotting the initial data')
    pyp.subplot(411)
    pyp.plot(f.data)

    pyp.subplot(412)
    print('Plotting the initial Fourier transfrom data')
    pyp.plot(xfreq, abs(fftdat[:len(fftdat)//2]))
    pyp.title('Wave dat of %s' % sys.argv[1])

    mv = np.mean(abs(fftdat)) # Mean value of the fourier transform
    coef = input("Enter the critical value coeficient 0-2 (default 1) to determine agressiveness of sound clearing. Current mean: {0}. ".format(mv))

    # Set the values for below critical to 0
    critical = float(coef) * mv
    print('Clearing the background noise')
    fftdat[abs(fftdat) < critical] = 0

    pyp.subplot(413)
    print('Plotting the new FFT without background noise')
    pyp.plot(abs(fftdat[:len(fftdat)//2]))

    pyp.subplot(414)
    print('Preforming the reverse Fourier transform')
    newdat = np.fft.irfft(fftdat)
    newdat = np.round(newdat).astype('int16')
    print('Plotting the new soundfile waveform')
    pyp.plot(newdat)

    spf = wave.open("rez.wav", 'w')
    spf.setparams(f.params)
    spf.writeframes(newdat)
    spf.close()

    pyp.show()

    print('File saved as rez.wav')