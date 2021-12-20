import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# 1 Pole LP Filter: H(s)  = 1 / (1+s)
b1 = [1]
a1 = [1, 1]

# 2 Pole LP Filter: H(s) = 1 / (s^2 + 2s + 1)
b2 = [1]
a2 = [1, 2, 1]

# 3 Pole LP Filter: H(s) = 1 / (s^3 + 3s^2 + 3s + 1)
b3 = [1]
a3 = [1, 3, 3, 1]

# 4 Pole LP Filter: H(s) = 1 / (s^4 + 4s^3 + 6s^2 + 4s + 1 )
b4 = [1]
a4 = [1, 4, 6, 4, 1]

# 1 Pole HP Filter: H(s)  = s / (s + 1)
b5 = [1, 0]
a5 = [1, 1]

# 2 Pole HP Filter: H(s) = s^2 / (s^2 + 2s + 1)
b6 = [1, 0, 0]
a6 = [1, 2, 1]

# 3 Pole HP Filter: H(s) = s^3 / (s^3 + 3s^2 + 3s + 1)
b7 = [1, 0, 0, 0]
a7 = [1, 3, 3, 1]

# 2 Pole BP Filter: H(s) = s / (s^2 + 2s + 1)
b8 = [1, 0]
a8 = [1, 2, 1]

# 3 Pole BP Filter: H(s) = s^2 / (s^4 + 4s^3 + 6s^2 + 4s + 1 )
b9 = [1, 0, 0]
a9 = [1, 4, 6, 4, 1]

#Experimental Function:
b10 = [0, 1, 1, 0]
a10 = [1, 3, 3, 1]

w1, h1 = signal.freqs(b1, a1, worN=np.logspace(-1, 3, 1000))
w2, h2 = signal.freqs(b2, a2, worN=np.logspace(-1, 3, 1000))
w3, h3 = signal.freqs(b3, a3, worN=np.logspace(-1, 3, 1000))
w4, h4 = signal.freqs(b4, a4, worN=np.logspace(-1, 3, 1000))
w5, h5 = signal.freqs(b5, a5, worN=np.logspace(-1, 3, 1000))
w6, h6 = signal.freqs(b6, a6, worN=np.logspace(-1, 3, 1000))
w7, h7 = signal.freqs(b7, a7, worN=np.logspace(-1, 3, 1000))
w8, h8 = signal.freqs(b8, a8, worN=np.logspace(-1, 3, 1000))
w9, h9 = signal.freqs(b9, a9, worN=np.logspace(-1, 3, 1000))
w10, h10 = signal.freqs(b10, a10, worN=np.logspace(-1, 3, 1000))

#plt.semilogx(w1, 20 * np.log10(abs(h1)))
#plt.semilogx(w2, 20 * np.log10(abs(h2)))
plt.semilogx(w3, 20 * np.log10(abs(h3)))
#plt.semilogx(w4, 20 * np.log10(abs(h4)))
#plt.semilogx(w5, 20 * np.log10(abs(h5)))
#plt.semilogx(w6, 20 * np.log10(abs(h6)))
plt.semilogx(w7, 20 * np.log10(abs(h7)))
#plt.semilogx(w8, 20 * np.log10(abs(h8)))
#plt.semilogx(w9, 20 * np.log10(abs(h9)))
plt.semilogx(w10, 20 * np.log10(abs(h10)))

#Experimental Plots:


plt.xlabel('Frequency')
plt.ylabel('Amplitude response [dB]')
plt.grid()
plt.show()
