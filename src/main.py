from src.operator import Operator
from src.population import Population

if __name__ == '__main__':
    population = Population()

    generations = 10

    # config population


    for x in range(0, generations):
        population.new_gen(population)
