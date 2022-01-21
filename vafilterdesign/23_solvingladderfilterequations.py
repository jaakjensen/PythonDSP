from sympy import Matrix, solve_linear_system
from sympy import Symbol
# Constants or Symbols
X = Symbol('X')
a0 = Symbol('a0')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
e = Symbol('g')
f = Symbol('g')
h = Symbol('g')
#g = Symbol('g')
j = Symbol('g')
k = Symbol('k')
Z = Symbol('Z')

#You can use the symbols above and substitute later 
#or you can define these as what they really are
#a = (g**3) / ((1+g)**4)
#b = (g**2) / ((1+g)**3)
#c = (g   ) / ((1+g)**2)
#d = (1   ) / ((1+g)   )

# Unknowns
W = Symbol('W')
U = Symbol('U')
Y1 = Symbol('Y1')
Y2 = Symbol('Y2')
Y3 = Symbol('Y3')
Y4 = Symbol('Y4')


m11 = (k*a*e*Z) / (1+e*Z)
m12 = ((k*a*Z)  / (1+e*Z)) + ((k*b*f*Z) / (1+f*Z))
m13 = ((k*b*Z)  / (1+f*Z)) + ((k*c*h*Z) / (1+h*Z))
m14 = ((k*c*Z)  / (1+h*Z)) + ((k*d*j*Z) / (1+j*Z))
m15 = ((k*d*Z)  / (1+j*Z))

m32 = e*(1+Z) - ((e*e*(Z+Z*Z)) / (1+e*Z))
m33 = (Z - 1) - ((e*  (Z+Z*Z)) / (1+e*Z))

m43 = f*(1+Z) - ((f*f*(Z+Z*Z)) / (1+f*Z))
m44 = (Z - 1) - ((f*  (Z+Z*Z)) / (1+f*Z))

m54 = h*(1+Z) - ((h*h*(Z+Z*Z)) / (1+h*Z))
m55 = (Z - 1) - ((h*  (Z+Z*Z)) / (1+h*Z))

m65 = j*(1+Z) - ((j*j*(Z+Z*Z)) / (1+j*Z))
m66 = (Z - 1) - ((j*  (Z+Z*Z)) / (1+j*Z))


system = Matrix(((-1, m11, m12, m13, m14, m15,  0),
                ( a0,   1,   0,   0,   0,   0,  a0*X),
                (  0, m32, m33,   0,   0,   0,  0),
                (  0,   0, m43, m44,   0,   0,  0),
                (  0,   0,   0, m54, m55,   0,  0),
                (  0,   0,   0,   0, m65, m66,  0)))

solution = solve_linear_system(system,W,U,Y1,Y2,Y3,Y4)

print(f"U = :{solution[U]}\n")
print(f"W = :{solution[W]}\n")
print(f"Y1 = :{solution[Y1]}\n")
print(f"Y2 = :{solution[Y2]}\n")
print(f"Y3 = :{solution[Y3]}\n")
print(f"Y4 = :{solution[Y4]}\n")


