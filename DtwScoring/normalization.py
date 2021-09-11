import numpy as np
import math

def vector_to_XY_arrays(vector):
    x = []
    y = []
    counter = 0
    for i in range(0, 75, 3):
        # if(vector[i + 2] >= 0.4):
        x.append(vector[i])
        y.append(vector[i + 1])
        # else:
            # x.append(None)
            # y.append(None)
        counter += 1
    return x, y

# x for x in L if x is not None
def normal_vector(vector):
    x, y  = vector_to_XY_arrays(vector)
    x_max = np.max(x)
    x_min = np.min(x)
    y_max = np.max(y)
    y_min = np.min(y)

    d_x = x_max - x_min
    d_y = y_max - y_min

    x_normal = []
    y_normal = []

    # t = math.sqrt(math.pow(d_x,2) + math.pow(d_y,2))

    # q = x[0]/t
    for i in x:
        x_normal.append(((i - x_min)/d_x))
    for i in y:
        y_normal.append(((i - y_min)/d_y))

    return x_normal, y_normal