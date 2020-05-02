from src.input import Operator
from src.population import Population

if __name__ == '__main__':
    population = Population()

    generations = 10

    # config population
    population.operator = Operator([-1, 1])  # x^2 -1
    population.population_size = 100
    population.population_discard = 0.2
    population.noise = 0.1
    population.crossover_options = [1, 2]
    population.mutation_options = [1, 2, 3, 4]

    for x in range(0, generations):
        best_result = population.new_gen(population)
        print("Best result: ", best_result)
