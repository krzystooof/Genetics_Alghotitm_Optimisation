from pyb.src.algorithm import Population
import json


def main():
    config = get_config()
    population = Population(config)

    while population.generation < 1000:  # TODO find good break condition
        for member in population.member_list:
            member.fitness = get_fitness(member.operator)
        population.new_gen()

    for member in population.member_list:
        member.fitness = get_fitness(member.operator)
    population.update_stats()
    print("Best member's fitness: ", population.best_member.fitness)
    print("Best member's operator: ", population.best_member.operator.values)

    # Saving final results into json
    final_results = {
        'calculated_result': population.best_member.operator.values,
    }
    with open("algorithm_results.json", "w") as write_file:
        json.dump(final_results, write_file)


def get_config():
    mutate = [1, 2, 3, 4]
    crossover = [1, 2]
    config_dict = {
        'population_size': 100,
        'population_discard': 0.5,
        'population_noise': 0.1,
        'population_chance_bonus': 2,
        'population_reverse_fitness': True,
        'member_config': {
            'random_low': -100,
            'random_high': 100,
            'member_mutation_options': mutate,
            'member_crossover_options': crossover
            }

    }
    return config_dict


def get_fitness(operator):  # simpleFitFunc, but in python
    return (operator.values[0] - 1.0)*(operator.values[0] - 1.0)


main()
