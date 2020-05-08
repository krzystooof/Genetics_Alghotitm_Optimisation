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
import random


class Population:
    """
        Class governing member reproduction and beeding mechanics.
        @author: Jakub Chodubski
        @version: 2.0
    """

    def __init__(self, operator, population_size, population_discard, noise, mutation_options,
                 crossover_options):  # Create random population
        # Variables to set (configuration)
        self.operator = operator

        # Size of population (Value <1-x>)
        self.population_size = population_size

        # Percentage of discarded members with each generation (Value <0-1>)
        self.population_discard = population_discard

        # Percentage of random mutations for each generation (Value <0-1>)
        self.noise = noise

        # 1 - random resetting - set random element to 0, 2 - swap mutation - swap two elements, 3 - scramble
        # mutation - shuffle random part, 4 - inversion mutation - invert random part
        self.mutation_options = mutation_options

        # 1 - one point, 2 - multi point
        self.crossover_options = crossover_options

        # generations specific variables - don't change
        self.generation = 0
        self.total_crossovers = 0
        self.best_fitness = 0
        self.member_list = []
        self.members_to_mutate = 0

        # Filling population with random members
        for x in range(0, self.population_size):
            self.member_list.append(Member(self.operator))

    def new_gen(self):
        """
        Generate new generation based on current generation. Some members will be discarded,
        new members will be created due to crossovers, mutations may appear.
        """
        self.check_config()
        self.sort_by_fitness()
        self.discard_unfit()
        self.breed_to_fill()
        self.apply_noise()
        # Population is now ready for testing

    def check_config(self):
        """Looks for changes in configuration"""
        # TODO
        pass

    def sort_by_fitness(self):
        self.member_list = sorted(self.member_list, key=lambda member: member.fitness)

    def discard_unfit(self):
        # Calculate how many members will be discarded
        unfit_n = self.population_discard * self.population_size
        # Calculate how many will stay
        fit_n = self.population_size - unfit_n
        # Rewrite fit members to new list
        new_list = []
        for x in range(0, fit_n):
            new_list.append(self.member_list[x])
        # Substitute lists
        self.member_list = new_list

    def get_statistics(self) -> dict:
        # TODO
        pass

    def breed_to_fill(self):
        # Assign crossover probability to each member
        self.assign_cross_chances()
        # Breed until population is full
        while len(self.member_list) < self.population_size:
            parent_1: Member = random.choice(self.member_list)
            parent_2: Member = random.choice(self.member_list)
            if random.random() < parent_1.crossover_chance * parent_2.crossover_chance:
                # TODO think about crossover options
                parent_1.crossover(random.choice(self.crossover_options), parent_2)

    def assign_cross_chances(self):
        # Get total fitness
        total_fitness = 0
        for member in self.member_list:
            total_fitness += member.fitness
        # Assign chances based on fitness
        for member in self.member_list:
            member.crossover_chance = member.fitness/total_fitness

    def apply_noise(self):
        # Calculate how many members will be mutated
        mutate_n = self.noise * self.population_size
        # Mutate members
        for x in range(0, mutate_n):
            mutating_member: Member = random.choice(self.member_list)
            mutating_member.mutate(random.choice(self.mutation_options))

    # TODO stat methods
    def get_population_info(self):
        # TODO move into get_stats()
        best_member = self.member_list[0]
        self.best_fitness = best_member.fitness
        self.__print_generation__()

        return best_member

    def __print_generation__(self):
        # TODO move into get_stats()
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
        self.crossover_chance = 0
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
