import numpy as np
from numpy import multiply as m

x2    = [1,0,0,0]
x1    = [0,1,0,0]
x0    = [0,0,1,0]
xm1   = [0,0,0,1]
a0    = np.add(x2,np.multiply(-1,x1))
a0    = np.add(a0,np.multiply(-1,xm1))
a0    = np.add(a0,x0)
a1    = np.add(xm1,np.multiply(-1,x0))
a1    = np.add(a1,np.multiply(-1,a0))
a2    = np.add(x1,np.multiply(-1,xm1))
a3    = x0

a_tuple = (a0,a1,a2,a3)
m = np.vstack(a_tuple)
m = np.rot90(np.fliplr(m))
print(m)
