"""Will continue to exist for pipeline purposes"""
from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config
from pyb.src.algorithm_core import FitnessDifferencesTooSmall
import json


def main():
    # Creating population
    population = Population(Config(noise=0.7, reverse=True, num_values=1))

    # You cant call new_gen without assigned fitness
    for member in population.member_list:
        member.fitness = get_fitness(member.operator)

    # Running algorithm until it can't get more accurate
    while True:
        # True can be changed to stop condition
        try:
            population.new_gen()
            for member in population.member_list:
                member.fitness = get_fitness(member.operator)
            print_stats(population)
        except FitnessDifferencesTooSmall:
            break

    # Saving final results into json
    final_results = {
        'calculated_result': population.best_member.operator.values,
    }
    with open("algorithm_results.json", "w") as write_file:
        json.dump(final_results, write_file)


def print_stats(population):
    print("Generation", str(population.generation) + ":")
    print("Best member: ", population.best_member.operator.values, " => ", population.best_member.fitness)


def get_fitness(operator):
    # HERE CHANGE WHAT FUNCTION IS IMPORTED \/\/\/
    from tests.sample_functions import simple_fit_func as fitness_func
    return fitness_func(operator.values)
    # After changing function make sure to update population's config - L11


main()
