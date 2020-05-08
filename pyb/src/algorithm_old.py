"""  A subset of all the possible  solutions to the given problem.

operator - input (see operator class)
population_size
population_discard - fraction of members to remove at each generation (float from 0.0 to 1.0)
noise - fraction of members to additionally mutate at each generation (float from 0.0 to 1.0)
mutation_options - list of mutation options, when creating new generation one option is randomly selected
    for each member: 1 - random resetting - set random element to 0, 2 - swap mutation - swap two elements,
    3 - scramble mutation - shuffle random part, 4 - inversion mutation - invert random part
crossover_options - list of crossover options, when creating new generation one option is randomly selected
    for each member: 1 - one point crossover, 2 - multi point crossover
"""
import math
import random


def sort_population_by_fitness(population):
    return sorted(population.member_list, key=lambda member: member.fitness)


class Population:
    """
        Class governing member reproduction and beeding mechanics.
    """

    def __init__(self, operator, population_size, population_discard, noise, mutation_options,
                 crossover_options):  # Create random population
        # Variables to set
        self.operator = operator
        self.population_size = population_size
        self.population_discard = population_discard
        self.noise = noise
        # 1 - random resetting - set random element to 0, 2 - swap mutation - swap two elements, 3 - scramble
        # mutation - shuffle random part, 4 - inversion mutation - invert random part
        self.mutation_options = mutation_options
        # 1 - one point, 2 - multi point
        self.crossover_options = crossover_options

        # generations specific variables - don't change
        self.generation = 0
        self.total_crossovers = 0
        self.random_fill = 0
        self.best_fitness = 0
        self.member_list = []
        self.members_to_mutate = 0

        # Filling population with random members
        for x in range(0, self.population_size):
            self.member_list.append(Member(self.operator))

    def new_gen(self, population):  # Create new population by mutating given population
        # Rewriting variables that won't change in new population
        self.population_discard = population.population_discard
        self.population_size = population.population_size
        self.generation = population.generation + 1
        self.mutation_options = population.mutation_options
        self.crossover_options = population.crossover_options

        # Calculating total members to discard and first discard index
        discard_members = math.floor(self.population_discard * self.population_size)
        discard_index_start = self.population_size - discard_members - 1

        # Sorting population by fitness
        sorted_list = sort_population_by_fitness(population)

        # Discarding unfit members
        for x in range(self.population_size, discard_index_start):
            sorted_list.pop(x)

        # Calculating total fitness of remaining members
        fitness_sum = 0
        for x in range(0, len(sorted_list)):
            fitness_sum += sorted_list[x].fitness

        # Calculating tickets for each remaining member. One ticket allows member for one "child"
        ticket_list = []
        for x in range(0, len(sorted_list)):
            tickets = sorted_list[x].fitness / fitness_sum
            tickets = int(tickets)
            ticket_list.insert(x, tickets)

        # Rewriting fit members to new population
        self.member_list = sorted_list
        self.population_size = len(self.member_list)

        # Adding mutations to new population

        crossovers_made = 0
        for x in range(0, len(ticket_list) - 1):
            for y in range(0, len(ticket_list) - 1):
                # mutations are crossover type
                crossover_type = random.choice(self.crossover_options)
                if ticket_list[x] >= 1 and ticket_list[y] >= 1:
                    self.member_list.append(self.member_list[x].crossover(crossover_type, self.member_list[y]))
                    crossovers_made += 1
        self.total_crossovers += crossovers_made

        self.population_size = len(self.member_list)

        # Adding new random members to the list
        self.random_fill = self.population_size - len(self.member_list)
        for x in range(0, self.random_fill):
            self.member_list.append(Member(self.operator))

        self.population_size = len(self.member_list)

        self.apply_noise()

        self.population_size = len(self.member_list)

    def apply_noise(self):
        self.members_to_mutate = self.noise * self.population_size
        for x in range(0, math.floor(self.members_to_mutate)):
            index = random.randint(0, self.population_size - 1)
            mutation_type = random.choice(self.mutation_options)
            self.member_list[index].mutate(mutation_type)

    def get_population_info(self):
        sort_population_by_fitness(self)
        best_member = self.member_list[0]
        self.best_fitness = best_member.fitness

        self.__print_generation__()

        return best_member

    def __print_generation__(self):
        print("==============================")
        print("Generation: ", self.generation)
        print("Population size: ", self.population_size)
        print("Best fitness: ", self.best_fitness)
        print("Total crossovers: ", self.total_crossovers)
        print("New random members: ", self.random_fill)
        print("Total random mutations: ", self.members_to_mutate)


class Member:
    """ One such solution to the given problem.

    operator - input (see operator class)
    """

    def __init__(self, operator):
        self.fitness = 0
        self.operator = operator

    def mutate(self, mutation_method):
        # self.input - list
        i = 0
        j = 0
        if len(self.operator.values) > 1:
            while j - i < 1:
                i = random.randint(0, len(self.operator.values) - 1)
                j = random.randint(i, len(self.operator.values) - 1)
        if mutation_method == 1:  # random resetting - set random element to 0
            self.operator.values[i] = 0
        elif mutation_method == 2:  # swap mutation - swap two elements
            self.operator.values[i], self.operator.values[j] = self.operator.values[j], self.operator.values[i]
        elif mutation_method == 3:  # scramble mutation - shuffle random part
            new_list = self.operator.values[i:j]
            random.shuffle(new_list)
            self.operator.values[i:j] = new_list
        elif mutation_method == 4:  # inversion mutation - invert random part
            self.operator.values[i:j] = list(reversed(self.operator.values[i:j]))

    def crossover(self, crossover_method, parent):
        # returns a child
        # self.operator.values - list
        i = 0
        j = 0
        while j - i < 1:
            length = len(self.operator.values)
            if len(parent.operator.values) < length:
                length = len(parent.operator.values)
            i = random.randint(0, length)
            j = random.randint(i, length)
        if crossover_method == 1:  # one point
            operator = Operator(self.operator.values[:i] + parent.operator.values[i:])
            return Member(operator)
        elif crossover_method == 2:  # multi point
            operator = Operator(self.operator.values[:i] + parent.operator.values[i:j] + self.operator.values[j:])
            return Member(operator)


class Operator:
    """ Class that implements polynomial input for member

    polynomial = sum from i to n of a(i) * x to the power of i ex 5x^5 - 4x2 + 1
    values - list of polynomial values reversed,
    ex polynomial = ax^2+b values=[b,0,a], (ax^2+0x+b)
    """

    def __init__(self, values):
        self.values = values
