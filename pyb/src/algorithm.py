"""
This module contains all code necessary to run genetic algorithm. It only provides bare minimum to
create population and mutate/breed members. Loop running this algorithm must be placed in order to use it.
@author: Jakub Chodubski
@author: Krzysztof Greczka
"""

import random
import math


class Population:
    """
        Class governing member reproduction and beeding mechanics.
        @author: Jakub Chodubski
        @version: 2.2
    """

    def __init__(self, config):
        """Creates new random population"""
        # Configuration variables
        self.population_size = 0
        self.population_discard = 0
        self.population_chance_bonus = 0
        self.noise = 0
        self.reverse = False
        self.break_generation = 1000
        self.member_config = {}

        # If config is available
        if config is not None:
            self.load_config(config)

        # Filling population with random members
            self.member_list = []
            for x in range(self.population_size):
                self.member_list.append(Member(self.member_config))

        # Statistics for current generation
            self.generation = 0
            self.best_member = self.member_list[0]
            self.total_crossovers = 0
            self.total_mutations = 0
            self.total_discarded = 0

    def new_gen(self):
        """
        Generate new generation based on current generation. Some members will be discarded,
        new members will be created due to crossovers, mutations may appear.
        """
        self.generation += 1
        self.update_stats()
        self.discard_unfit()
        self.breed_to_fill()
        self.apply_noise()
        # Population is now ready for testing

    def sort_by_fitness(self):
        if self.reverse:
            # TODO: inplace sort
            # think using arrays
            self.member_list = sorted(self.member_list, key=lambda member: member.fitness, reverse=False)
        else:
            self.member_list = sorted(self.member_list, key=lambda member: member.fitness, reverse=True)

    def discard_unfit(self):
        # Calculate how many members will be discarded
        self.total_discarded = math.floor(self.population_discard * self.population_size)
        # Calculate how many will stay
        fit_n = self.population_size - self.total_discarded
        # Rewrite fit members to new list
        new_list = []
        for x in range(fit_n):
            # If statement discards nan and inf values
            if not math.isnan(self.member_list[x].fitness) and not math.isinf(self.member_list[x].fitness):
                new_list.append(self.member_list[x])
            else:
                self.total_discarded += 1
        # Substitute lists
        self.member_list = new_list

    def breed_to_fill(self):
        # Assign crossover probability to each member
        self.assign_cross_chances()
        # Breed until population is full
        self.total_crossovers = 0
        new_members = []
        while len(new_members) < self.population_size - len(self.member_list):
            parent_1 = random.choice(self.member_list)
            parent_2 = random.choice(self.member_list)
            if random.random() < parent_1.crossover_chance * parent_2.crossover_chance:
                new_members.append(parent_1.crossover(parent_2))
        self.total_crossovers = len(new_members)
        self.member_list += new_members

    def assign_cross_chances(self):
        """Assigns crossover chances to every member of population based on fitness"""
        self.sort_by_fitness()
        step = 1/len(self.member_list)
        for x in range(len(self.member_list)):
            self.member_list[x].crossover_chance = 1 - (step * x)

            # Check for weird values
            if math.isnan(self.member_list[x].fitness) or math.isinf(self.member_list[x].fitness):
                self.member_list[x].crossover_chance = 0

    def apply_noise(self):
        # Calculate how many members will be mutated
        self.total_mutations = math.floor(self.noise * self.population_size)
        # Mutate members
        for x in range(self.total_mutations):
            mutating_member = random.choice(self.member_list)
            mutating_member.mutate()

    def load_config(self, config):
        """
        Loads configuration variables. Takes dictionary as argument. This dictionary must contain fields:
          - population_size - Size of population (Value <1-x>)
          - population_discard - Percentage of discarded members with each generation (Value <0-1>)
          - population_noise - Percentage of random mutations for each generation (Value <0-1>)
          - population_chance_bonus - Higher values = less accurate crossovers = faster runtime (Value <1-x>)
          - population_reverse_fitness - Tells algorithm which is better: Lower fitness or higher. (Value [True,False])
          - member_config - Member's config dict. More on that in Member.__init__()
        """

        self.population_size = config['population_size']
        self.population_discard = config['population_discard']
        self.population_chance_bonus = config['population_chance_bonus']
        self.break_generation = config['generations']
        self.noise = config['population_noise']
        self.reverse = config['population_reverse_fitness']
        self.member_config = config['member_config']

    def update_stats(self):
        self.sort_by_fitness()
        self.best_member = self.member_list[0]


class Member:
    """ One such solution to the given problem.

    operator - input (see operator class)
    @author: Krzysztof Greczka
    """

    def __init__(self, config):
        """
        Member's config:
            - random_low - initial values lower limit
            - random_high - initial values higher limit
            - num_values - how many values does operator keep
            - member_mutation_options - List of allowed mutation types. Possible values:
                1. Random resetting (set random element to 0)
                2. Swap mutation (swap two elements)
                3. Scramble mutation (shuffle random part)
                4. Inversion mutation (invert random part)
            - member_crossover_options - List of allowed crossover types. Possible values:
                1. One point
                2. Multi point
        """
        self.fitness = 0.0
        self.crossover_chance = 0

        self.random_low = config['random_low']
        self.random_high = config['random_high']
        self.num_values = config['num_values']
        self.mutation_options = config['mutation_options']
        self.crossover_options = config['crossover_options']
        self.config = config
        # make random operator
        operator_list = []
        for x in range(self.num_values):
            operator_list.append(random.uniform(self.random_low, self.random_high))
        self.operator = Operator(operator_list)

    def mutate(self):
        mutation_method = random.choice(self.mutation_options)
        # self.input - list
        i = 0
        j = 0
        if len(self.operator.values) > 1:
            while j - i < 1:
                i = random.randint(0, len(self.operator.values) - 1)
                j = random.randint(i, len(self.operator.values) - 1)
        if mutation_method == 1:  # random resetting - sets random number to random value
            self.operator.values[i] *= random.uniform(self.random_low, self.random_high)
        elif mutation_method == 2:  # swap mutation - swap two elements
            self.operator.values[i], self.operator.values[j] = self.operator.values[j], self.operator.values[i]
        elif mutation_method == 3:  # scramble mutation - shuffle random part
            new_list = self.operator.values[i:j]
            shuffle(new_list)
            self.operator.values[i:j] = new_list
        elif mutation_method == 4:  # inversion mutation - invert random part
            self.operator.values[i:j] = [(reversed(self.operator.values[i:j]))]

    def crossover(self, parent):
        crossover_method = random.choice(self.crossover_options)
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
            to_ret = Member(self.config)
            to_ret.operator = operator
            return to_ret
        elif crossover_method == 2:  # multi point
            operator = Operator(self.operator.values[:i] + parent.operator.values[i:j] + self.operator.values[j:])
            to_ret = Member(self.config)
            to_ret.operator = operator
            return to_ret


class Operator:
    """ Class that implements polynomial input for member

    polynomial = sum from i to n of a(i) * x to the power of i ex 5x^5 - 4x2 + 1
    values - list of polynomial values reversed,
    ex polynomial = ax^2+b values=[b,0,a], (ax^2+0x+b)
    @author: Krzysztof Greczka
    """

    def __init__(self, values):
        self.values = values


def shuffle(to_shuffle):
    """Shuffles lists with Fisher–Yates algorithm for performance"""
    for x in range(len(to_shuffle)):
        y = random.randint(x)
        to_shuffle[x], to_shuffle[y] = to_shuffle[y], to_shuffle[x]
