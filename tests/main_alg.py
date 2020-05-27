# Draft for grzegorz
# This file will not exists, it just demonstrates how Algorithm class will be invoked

import pyb.src.algorithm
from .sample_functions import quadratic

alg = Algorithm(quadratic, values=1, population=100, accuracy=0.0001, rand_low=-100, rand_high=100, reverse=True)

result = agl.run()
print("This function has a minimum of: " + str(result))
