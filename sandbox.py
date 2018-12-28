import numpy as np

signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=float)
fourier = np.fft.fft(signal)
print(fourier)
print(signal.size)
freq = np.fft.fftfreq(signal.size, d=0.1)
print(freq)