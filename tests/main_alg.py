"""
Draft for @Grzegorz
This file will not exists, it just demonstrates how Algorithm class will be invoked
"""
from pyb.src.algorithm import Algorithm
from tests.sample_functions import sample_function

alg = Algorithm(sample_function, values=1, population=100, accuracy=0.0001, rand_low=-100, rand_high=100,
                reverse=True)
# Quadratic will sometimes throw an exception. If this happens run() function must be exited immediately.
# After run() function is invoked once again it must continue from where it was interrupted.
# Exception type will be "StopIteration".

while not alg.is_finished:
    # alg.is_finished must be False if run() was exited due to "StopIteration" exception, True if accuracy was reached.
    alg.run()

result = alg.result
# result is best member's operator
print("This function has a minimum of: " + str(result))

