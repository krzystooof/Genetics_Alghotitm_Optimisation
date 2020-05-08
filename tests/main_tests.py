from pyb.src.algorithm import Population


def main():
    config = get_config()
    population = Population(config)

    while population.generation < 100:  # TODO find good break condition
        for member in population.member_list:
            member.fitness = get_fitness(member.operator)
        population.update_stats()
        population.new_gen()

    population.update_stats()
    print("Best member's fitness: ", population.best_member.fitness)
    print("Best member's operator: ", population.best_member.operator.values)
    # TODO algorithm ended. Save final results


def get_config():
    mutate = [1, 2, 3, 4]
    crossover = [1, 2]
    config_dict = {
        'population_size': 100,
        'population_discard': 0.5,
        'population_noise': 0.3,
        'population_chance_bonus': 5,
        'member_mutation_options': mutate,
        'member_crossover_options': crossover
    }
    return config_dict


def get_fitness(operator):  # simpleFitFunc, but in python
    return (operator.values[0] - 1)*(operator.values[0] - 1)


main()
