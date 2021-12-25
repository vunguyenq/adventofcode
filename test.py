import numpy as np
a = np.arange(100, dtype=int).reshape(10, 10)
b = '\n'.join('\t'.join(str(x) for x in y) for y in a)
print(b)