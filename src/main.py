from src.population import Population

if __name__ == '__main__':
    population = Population()

    # TODO config population
    generations = 0

    for x in range(0, generations):
        population.new_gen(population)