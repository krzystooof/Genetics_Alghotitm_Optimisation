import json

from pyb.src.port import VCP
from pyb.src.algorithm_old import Operator
from pyb.src.algorithm_old import Population

# Create Virtual Comm Port to communicate with desktop
usb = VCP


def main():
    """Main function. First to run"""

    # wait for input from USB
    configuration = usb.read()
    while configuration["type"] is 0:
        configuration = usb.read()

    # Reading configuration values
    operator = Operator(read_from_dictionary(configuration, "operator", [-1, 1]))
    generations = read_from_dictionary(configuration, "generations", 10)
    population_size = read_from_dictionary(configuration, "population_size", 100)
    population_discard = read_from_dictionary(configuration, "population_discard", 10)
    noise = read_from_dictionary(configuration, "noise", 0.1)
    mutation_options = read_from_dictionary(configuration, "mutation_options", [1, 2, 3, 4])
    crossover_options = read_from_dictionary(configuration, "crossover_options", [1, 2])

    # Comment here
    population = Population(operator, population_size, population_discard, noise, mutation_options, crossover_options)
    test_population(population)
    best_member = population.get_population_info()
    print("Best result: ", best_member.operator.values)

    # Comment here
    generations_values = []  # List for further saving results to json
    for x in range(0, generations):
        population.new_gen(population)
        test_population(population)
        best_member = population.get_population_info()
        generations_values.append(best_member.operator.values)
        print("Best result: ", best_member.operator.values)

    # Save results
    results = {f'generation_{counter}': value for counter, value in enumerate(generations_values)}
    with open("../../tests/algorithm_results.json", "w") as outfile:
        json.dump(results, outfile, indent=4)

    # Comment here
    usb.attach("best_member_values", best_member.operator.values)
    usb.attach("best_member_fitness", best_member.fitness)


def read_from_dictionary(dictionary, item, default):
    try:
        return dictionary[item]
    except KeyError:
        # item not in dictionary
        return default


def test_population(population):
    """Sends every member of given population for testing on desktop side"""
    # send data to calculate fitness and save reply
    for member in population.member_list:
        usb.attach('operator', member.operator)
        usb.send()
        reply = usb.read()
        while reply["type"] is 0:
            reply = usb.read()
        try:
            member.fitness = reply["fitness"]
        except KeyError:
            # item not in dictionary
            member.fitness = 0


main()
