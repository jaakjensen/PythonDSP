import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#Define your function here. Use z^-1 form.
#If len(a) != len(b), don't append the smaller
#len array with zeros
a = [0.0798,0.0798,0.0798,0.0798]
b = [1,-1.556,1.272,-0.398]

zero,pole,gain = signal.tf2zpk(a,b)
print(f'Zeroes = {np.abs(zero)}')
print(f'Poles = {np.abs(pole)}')


def f(x, y):
    c = np.zeros(np.shape(x), dtype=complex)
    result1 = np.zeros(np.shape(x), dtype=complex)
    result2 = np.zeros(np.shape(x), dtype=complex)
    c.real = x
    c.imag = y

    gLen = max(len(a),len(b))

    for i in reversed(range(0,len(a))):
        if(gLen == len(a)):
            result1+=(np.power(c,i) * a[i])
        else:
            result1+=(np.power(c,i+gLen-1) * a[i])

    for i in reversed(range(0,len(b))):
        if(gLen == len(b)):
            result2+=(np.power(c,i) * b[i])
        else:
            result2+=(np.power(c,i+gLen-1) * b[i])

    return np.abs(result1)/np.abs(result2)

#Calculate X,Y,Z
x = np.linspace(-1.5, 1.5, 40)
y = np.linspace(-1.5, 1.5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

#Plot X,Y,and Z
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
ax.set_title('Z-Plane');

# Plot the unit circle
theta = np.linspace(0, 2*np.pi, 100)
xline = np.sin(theta)
yline = np.cos(theta)
zline = f(xline,yline)
ax.plot3D(xline, yline, zline, 'black', linewidth=2)

#Plot poles and zeros on Z=0 plane
xzeros = np.abs(zero) * np.cos(np.angle(zero))
yzeros = np.abs(zero) * np.sin(np.angle(zero))
zzeros = np.zeros(np.shape(xzeros))

xpoles = np.abs(pole) * np.cos(np.angle(pole))
ypoles = np.abs(pole) * np.sin(np.angle(pole))
zpoles = np.zeros(np.shape(xpoles))

ax.scatter3D(xzeros, yzeros, zzeros, s=100, c='g')
ax.scatter3D(xpoles, ypoles, zpoles, s=100, c='r')

ax.set_xlabel('Real')
ax.set_ylabel('Imaginary')
ax.set_zlim(0,np.max(zline))
plt.show()
