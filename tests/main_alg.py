# Draft for grzegorz
# This file will not exists, it just demonstrates how Algorithm class will be invoked

import pyb.src.algorithm
from sample_functions import quadratic
class Algorithm:
    def __init__(self, function_type,
                 values,
                 population,
                 accuracy,
                 rand_low,
                 rand_high,
                 reverse):
        self.reverse = reverse
        self.rand_high = rand_high
        self.rand_low = rand_low
        self.accuracy = accuracy
        self.population = population
        self.values = values
        self.function_type = function_type



    def run(self):


        return 0




alg = Algorithm(quadratic, values=1, population=100, accuracy=0.0001, rand_low=-100, rand_high=100, reverse=True)

result = alg.run()
print("This function has a minimum of: " + str(result))
