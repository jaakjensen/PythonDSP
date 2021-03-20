
import numpy as np

arr = np.array([[5]])

rowVec = np.array([[1,2,3,4]])

colVec = np.array([[1],[2],[3],[4]])

charVec = np.array(['h','e','l','l','o'])

strCol = np.array([['one'],['two']])

strErr = np.array([['one'],['two'],['three']])

strRow1 = np.array(['one','two','three'])

strRow2 = np.array(['one','three','five'])

rowConcat = np.concatenate((rowVec, arr), axis = 1)

colConcat = np.concatenate((colVec, arr), axis = 0)

print(f'{arr}\n')
print(f'{rowVec}\n')
print(f'{colVec}\n')
print(f'{charVec}\n')
print(f'{strCol}\n')
print(f'{strErr}\n')
print(f'{strRow1}\n')
print(f'{strRow2}\n')
print(f'{rowConcat}\n')
print(f'{colConcat}\n')


