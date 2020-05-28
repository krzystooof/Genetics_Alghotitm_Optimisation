"""
This module contains all code necessary to run genetic algorithm. It only provides bare minimum to
create population and mutate/breed members. Loop running this algorithm must be placed in order to use it.
@author: Jakub Chodubski
@author: Krzysztof Greczka
"""

import random
import math


class FitnessDifferencesTooSmall(Exception):
    def __init__(self, message="Algorithm cannot produce more accurate result. Please stop invoking new_gen()"):
        super().__init__(message)


class Config:
    """Keeps data so it can be passed easily"""
    def __init__(self, population_size=100,
                 population_discard=0.5,
                 population_chance_bonus=1,
                 noise=0.5,
                 reverse=False,
                 random_low=-100,
                 random_high=100,
                 num_values=10,
                 crossover_options=None):
        """
        Loads configuration variables. Variables:
          - population_size - Size of population (Value <1-x>)
          - population_discard - Percentage of discarded members with each generation (Value <0-1>)
          - noise - Percentage of random mutations for each generation (Value <0-1>)
          - population_chance_bonus - Higher values = less accurate crossovers = faster runtime (Value <1-x>)
          - reverse - Tells algorithm which is better: Lower fitness or higher. (Value [True,False])
          - random_low - initial values lower limit
          - random_high - initial values higher limit
          - num_values - how many values does operator keep
          - member_crossover_options - List of allowed crossover types. Possible values:
              1. One point
              2. Multi point
        """
        self.crossover_options = [1, 2]
        if crossover_options is not None:
            self.crossover_options = crossover_options
        self.population_size = population_size
        self.population_discard = population_discard
        self.population_chance_bonus = population_chance_bonus
        self.noise = noise
        self.reverse = reverse
        self.random_low = random_low
        self.random_high = random_high
        self.num_values = num_values


class Population:
    """
        Class governing member reproduction and beeding mechanics. Throws ValueError when no further generations
        are possible.
        @author: Jakub Chodubski
        @version: 2.4
    """

    def __init__(self, config=Config()):
        """Creates new random population"""
        # Configuration variables
        self.config = config

        # Filling population with random members
        self.member_list = []
        for x in range(self.config.population_size):
            self.member_list.append(Member(self.config))
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
        # Population is now ready for testing

    def sort_by_fitness(self):
        """Sorts member_list so [0] is best member"""
        if self.config.reverse:
            self.member_list.sort(key=lambda member: member.fitness, reverse=False)
        else:
            self.member_list.sort(key=lambda member: member.fitness, reverse=True)

    def update_stats(self):
        self.sort_by_fitness()
        self.best_member = self.member_list[0]

    def discard_unfit(self):
        # Calculate how many members will be discarded
        self.total_discarded = math.floor(self.config.population_discard * self.config.population_size)
        # Calculate how many will stay
        fit_n = self.config.population_size - self.total_discarded
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
        while len(new_members) < self.config.population_size:
            parent_1 = random.choice(self.member_list)
            parent_2 = random.choice(self.member_list)
            if random.random() < parent_1.crossover_chance * parent_2.crossover_chance:
                new_members.append(parent_1.crossover(parent_2))
        self.total_crossovers = len(new_members)
        self.member_list = new_members

    def assign_cross_chances(self):
        self.sort_by_fitness()
        high = self.member_list[0].fitness
        low = self.member_list[len(self.member_list) - 1].fitness

        if high < low:
            high, low = low, high

        high -= low
        try:
            for member in self.member_list:
                # Catch weird values
                if math.isnan(member.fitness) or math.isinf(member.fitness):
                    member.crossover_chance = 0
                    continue

                fitness = member.fitness - low
                chance = fitness / high
                if self.config.reverse:
                    member.crossover_chance = 1 - chance
                else:
                    member.crossover_chance = chance
        except ZeroDivisionError:
            raise FitnessDifferencesTooSmall


class Member:
    """ One such solution to the given problem.

    operator - input (see operator class)
    @author: Krzysztof Greczka
    """

    def __init__(self, config):
        """Config must be of config class"""
        self.fitness = 0.0
        self.crossover_chance = 0
        self.config = config

        # make random operator
        operator_list = []
        for x in range(self.config.num_values):
            operator_list.append(random.uniform(self.config.random_low, self.config.random_high))
        self.operator = Operator(operator_list)

    def mutate_value(self, index, scale):
        # value = value +- scale * n
        if random.random() > 0.5:
            self.operator.values[index] += scale * normal(0, 2)
        else:
            self.operator.values[index] -= scale * normal(0, 2)

    def crossover(self, parent):
        """Returns a child of self and parent"""
        i = 0
        j = 0
        to_ret = Member(self.config)
        operator = None

        # Random values needed later
        while j - i < 1:
            length = len(self.operator.values)
            if len(parent.operator.values) < length:
                length = len(parent.operator.values)
            i = random.randint(0, length)
            j = random.randint(i, length)

        # Make a new operator
        crossover_method = random.choice(self.config.crossover_options)
        if crossover_method == 1:  # one point
            operator = Operator(self.operator.values[:i] + parent.operator.values[i:])
        elif crossover_method == 2:  # multi point
            operator = Operator(self.operator.values[:i] + parent.operator.values[i:j] + self.operator.values[j:])
        to_ret.operator = operator

        # Mutate child
        if random.random() < self.config.noise:
            index = random.randint(0, len(self.operator.values) - 1)
            scale = parent.operator.values[index] - self.operator.values[index]
            to_ret.mutate_value(index, scale)

        # Return child
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


def normal(x, y):
    return random.uniform(x, y)  # TODO get uniform with normal distribution
