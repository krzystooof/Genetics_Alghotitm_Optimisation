import json

from pyb.src.algorithm_old import Operator
from pyb.src.algorithm_old import Population

# Reading values

operator = [-1, 1]
generations = 10
population_size = 100
population_discard = 10
noise = 0.1
mutation_options = [1, 2, 3, 4]
crossover_options = [1, 2]

# Comment here
population = Population(operator, population_size, population_discard, noise, mutation_options, crossover_options)
test_population(population)
best_member = population.get_population_info()
print("Best result: ", best_member.operator.values)

# Comment here
generations_values = []  # List for further saving results to json
for x in range(0, generations):
    population.new_gen(population)
    test_population(population)
    best_member = population.get_population_info()
    generations_values.append(best_member.operator.values)
    print("Best result: ", best_member.operator.values)

# Save results
# TODO: This must be saved but cannot stay in main.py as its prepared for execution on STM
results = {f'generation_{counter}': value for counter, value in enumerate(generations_values)}
with open("../../tests/algorithm_results.json", "w") as outfile:
    json.dump(results, outfile, indent=4)
