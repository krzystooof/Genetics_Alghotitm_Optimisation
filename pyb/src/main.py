import json
from input import Operator
from population import Population

if __name__ == '__main__':

    generations = 10

    # config population
    operator = Operator([-1, 1])  # x^2 -1
    population_size = 100
    population_discard = 0.2
    noise = 0.1
    mutation_options = [1, 2, 3, 4]
    crossover_options = [1, 2]

    population = Population(operator, population_size, population_discard, noise, mutation_options, crossover_options)

    generations_values = []

    for x in range(generations):
        best_result = population.new_gen(population)
        results_copy = best_result.values.copy()
        print("Best result: ", results_copy)
        print("Population generation: ", population.generation)
        print((population.generation, x + 1))
        generations_values.append(results_copy)

    # Results of algorithm
    results = {f'generation_{counter}': value for counter, value in enumerate(generations_values)}

    with open("tests/algorithm_results.json", "w") as outfile:
        json.dump(results, outfile, indent=4)
