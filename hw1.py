import numpy as np
import math

a = np.arange(2,27)
print(a)

b = a.reshape(5,5)
print(b)
b[1:4, 1:4] = 0

M=b
print(M)
M=M@M
print(M)

sum = 0
for i in range(5):
    sum += M[0][i] **2
sum = math.sqrt(sum)
print(sum)
