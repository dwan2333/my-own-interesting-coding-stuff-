import numpy as np

data = np.arange(10)
print(data)
arr_slice  = data[5:8].copy()

print(arr_slice)

arr_slice[1] = 1234

print(arr_slice)