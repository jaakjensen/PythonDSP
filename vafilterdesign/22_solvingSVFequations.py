from sympy import Matrix, solve_linear_system
from sympy import Symbol
X = Symbol('X')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
d = Symbol('d')
Z = Symbol('Z')
W = Symbol('W')
Yhp = Symbol('Yhp')
Ybp = Symbol('Ybp')
Ylp = Symbol('Ylp')

system = Matrix(((b*Z*c,Z*(b+d),Z,-1,0),
                (-1,0,0,-a,-a*X),
                (c*(1+Z),Z-1,0,0,0),
                (0,d*(1+Z),Z-1,0,0)))

solution = solve_linear_system(system,Yhp,Ybp,Ylp,W)

print(f"Yhp = :{solution[Yhp]}\n")
print(f"Ybp = :{solution[Ybp]}\n")
print(f"Ylp = :{solution[Ylp]}\n")
