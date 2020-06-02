import json
from pyb.src.algorithm import Algorithm
from tests.fitness_functions import simple_fit_func

ptmag = Algorithm(simple_fit_func, num_values=1, reverse=True, print_logs=True)

result = ptmag.optimise()
print('Time: ', ptmag.elapsed_time)

# Saving final results into json
with open("algorithm_results.json", "w") as write_file:
    json.dump({
        'calculated_result': result,
    }, write_file)
