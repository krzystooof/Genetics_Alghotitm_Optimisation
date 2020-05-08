from pyb.src.algorithm import Operator
from pyb.src.algorithm import Population
from pyb.src.port import VCP


def read_from_dictionary(dictionary, item, default):
    try:
        return dictionary[item]
    except KeyError:
        # item not in dictionary
        return default


def calculate_fitness(population):
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


usb = VCP

# communicate with Desktop to calculate fitness
# return output

# wait for input from USB
configuration = usb.read()
while configuration["type"] is 0:
    configuration = usb.read()

operator = Operator(read_from_dictionary(configuration, "operator", [-1, 1]))
generations = read_from_dictionary(configuration, "generations", 10)
population_size = read_from_dictionary(configuration, "population_size", 100)
population_discard = read_from_dictionary(configuration, "population_discard", 10)
noise = read_from_dictionary(configuration, "noise", 0.1)
mutation_options = read_from_dictionary(configuration, "mutation_options", [1, 2, 3, 4])
crossover_options = read_from_dictionary(configuration, "crossover_options", [1, 2])

population = Population(operator, population_size, population_discard, noise, mutation_options, crossover_options)
calculate_fitness(population)
best_member = population.get_population_info()
print("Best result: ", best_member.operator.values)

for x in range(0, generations):
    population.new_gen(population)
    calculate_fitness(population)
    best_member = population.get_population_info()
    print("Best result: ", best_member.operator.values)

usb.attach("best_member_values", best_member.operator.values)
usb.attach("best_member_fitness", best_member.fitness)
