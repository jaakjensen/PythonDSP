import numpy as np
from scipy import signal
from plot_zplane import zplane
import matplotlib.pyplot as plt

b = np.array([2,2])
a = np.array([1,-1.25])

zplane(b,a)
