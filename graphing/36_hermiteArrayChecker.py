import numpy as np
from numpy import multiply as m

x2    = [1,0,0,0]
x1    = [0,1,0,0]
x0    = [0,0,1,0]
xm1   = [0,0,0,1]
c     = np.add(np.multiply(0.5,x1),np.multiply(-0.5,xm1))
v     = np.add(x0,np.multiply(-1,x1))
w     = np.add(c,v)
a     = np.add(w,v)
a     = np.add(a,np.add(np.multiply(0.5,x2),np.multiply(-0.5,x0)))
bneg  = np.add(w,a)
bneg2 = np.multiply(-1,bneg)

a_tuple = (a,bneg2,c,x0)
m = np.vstack(a_tuple)
m = np.rot90(np.fliplr(m))
print(m)
