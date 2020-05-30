import json
from pyb.src.algorithm import Algorithm
from tests.fitness_functions import simple_fit_func

ptmag = Algorithm(simple_fit_func, num_values=1, reverse=True, log=True)

result = ptmag.optimise()
print('Time: ', ptmag.time)
# Saving final results into json
final_results = {
    'calculated_result': result,
}
with open("algorithm_results.json", "w") as write_file:
    json.dump(final_results, write_file)
