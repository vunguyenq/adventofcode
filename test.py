import numpy as np
p = 5
distance_func = lambda x: (x-p)(x-p+1)/2
x = np.array([1, 2, 3, 4, 5])
f = lambda x: (x-p)*(x-p+1)/2
squares = f(x)
print(squares)