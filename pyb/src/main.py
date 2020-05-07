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

    generation_value1234 = [[0, 0], [100, 100], [100, 100], [100, 100], [100, 100], [100, 100], [100, 100], [100, 100],
                            [100, 100], [100, 100], [100, 100]]

    for x in range(generations):
        best_result = population.new_gen(population)
        print("Best result: ", best_result.values)
        print("Population generation: ", population.generation)
        print((population.generation, x+1))
        if population.generation == x+1:
            generation_value1234[x + 1] = best_result.values

        print("WYNIKI: ", generation_value[0])
        print("WYNIKI: ", generation_value1234[1])
        print("WYNIKI: ", generation_value1234[2])
        print("WYNIKI: ", generation_value1234[3])
        print("WYNIKI: ", generation_value1234[4])
        print("WYNIKI: ", generation_value1234[5])
        print("WYNIKI: ", generation_value1234[6])
        print("WYNIKI: ", generation_value1234[7])
        print("WYNIKI: ", generation_value1234[8])
        print("WYNIKI: ", generation_value1234[9])
        print("WYNIKI: ", generation_value1234[10])
















    # Data to be written
    results = {
        "gen0": generation_value1234[0],
        "gen1": generation_value1234[1],
        "gen2": generation_value1234[2],
        "gen3": generation_value1234[3],
        "gen4": generation_value1234[4],
        "gen5": generation_value1234[5],
        "gen6": generation_value1234[6],
        "gen7": generation_value1234[7],
        "gen8": generation_value1234[8],
        "gen9": generation_value1234[9],
        "gen10": generation_value1234[10]

    }
    with open("tests/results1.json", "w") as outfile:
        json.dump(results, outfile)