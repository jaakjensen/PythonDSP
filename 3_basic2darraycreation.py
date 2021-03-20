
import numpy as np

mat1 = np.array([[1,2,3],[4,5,6]])

mat2 = np.array([[1,2],[3,4],[5,6]])

mat3 = np.concatenate((mat1, [[7,8,9]]), axis = 0)

mat4 = np.concatenate((mat2, [[7,8]]), axis = 0)

print(f'{mat1}\n')
print(f'{mat2}\n')
print(f'{mat3}\n')
print(f'{mat4}\n')


