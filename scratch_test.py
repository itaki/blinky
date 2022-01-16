# import time

# start_time = time.time()

# stop = input("stop the tape!")
# stop_time = time.time()
# print (stop_time)

# total_time = stop_time - start_time
# print(total_time)

# keyboard version of blinky
import numpy as np
a_array =np.array([1,2,3,4])
b_array = np.array([3,4,5])
bool_a_b = np.isin(a_array, b_array)
print(bool_a_b)