from pyb.src.input import Operator
from pyb.src.population import Population

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

    for x in range(0, generations):
        best_result = population.new_gen(population)
        print("Best result: ", best_result.values)
