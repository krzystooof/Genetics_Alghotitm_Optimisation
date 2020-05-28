import json
from pyb.src.algorithm import Algorithm
from tests.fitness_functions import simple_fit_func

ptmag = Algorithm(simple_fit_func, variables=1)

result = ptmag.optimise()

# Saving final results into json
final_results = {
    'calculated_result': result,
}
with open("algorithm_results.json", "w") as write_file:
    json.dump(final_results, write_file)

