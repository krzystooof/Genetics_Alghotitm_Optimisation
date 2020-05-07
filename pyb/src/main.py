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

    generation_value = []
    for x in range(generations):
        best_result = population.new_gen(population).values
        a = best_result.copy()
        print("Best result: ", a)
        print("Population generation: ", population.generation)
        print((population.generation, x + 1))
        generation_value.append(a)

    print(generation_value)

    # Results of algorithm
    results = {
        "gen1": generation_value[0],
        "gen2": generation_value[1],
        "gen3": generation_value[2],
        "gen4": generation_value[3],
        "gen5": generation_value[4],
        "gen6": generation_value[5],
        "gen7": generation_value[6],
        "gen8": generation_value[7],
        "gen9": generation_value[8],
        "gen10": generation_value[9],

    }
    with open("tests/results.json", "w") as outfile:
        json.dump(results, outfile)
