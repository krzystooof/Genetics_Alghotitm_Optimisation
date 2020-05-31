"""
This module contains necessary code to start work of algorithm. It includes setting parameters for algorithm,
running of algorithm and calculating the result of algorithm .
@author: Grzegorz Drozda
@author: Roland Jałoszyński
"""
from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config
from pyb.src.algorithm_core import FitnessDifferencesTooSmall
import math
import time


class Algorithm:

    """Keeps data so it can be passed easily

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
        - fitness_callback - the function, which algorithm works for
        - print_logs - prints the stats of generations in algorithm
        - accuracy - algorithm accuracy that affects the start of the stop condition
        - best_fitness_in_gen - List of best fitness member in generations
        - list_coefficient_of_variation - List of coefficient of variation in generations
        - time - amount of time of working algorithm
    """
    def __init__(self, fitness_callback, num_values, log=False, accuracy=0.0005, **kwargs):

        self.population = Population(num_values=num_values, **kwargs)
        self.execute_callback = fitness_callback
        self.accuracy = accuracy
        self.best_fitness_in_gen = []
        self.print_logs = log
        # time of algorithm
        self.time = 0
        # list for coefficient of variation
        self.list_coefficient_of_variation = []

    def optimise(self):
        start_timer = time.time()
        stop_timer = 0
        while self.population.generation < self.population.config.population_size:
            try:
                stop_timer = time.time()
                self.time = stop_timer - start_timer
                self.__calculate_generation_fitness()
                start_timer = time.time()
            except StopIteration:
                raise
            else:
                self.best_fitness_in_gen.append(self.population.best_member.operator.values[0])
                self.population.update_stats()
                if self.print_logs:
                    self.__print_stats()
                if self.__check_stop_condition(self.best_fitness_in_gen):
                    return self.population.best_member.operator.values
                try:
                    self.population.new_gen()
                except FitnessDifferencesTooSmall:
                    stop_timer = time.time()
                    self.time = stop_timer - start_timer + self.time
                    return self.population.best_member.operator.values

    def __calculate_generation_fitness(self):
        for member in self.population.member_list:
            member.fitness = self.execute_callback(member.operator.values)

    # using standard deviation
    def __check_stop_condition(self, best_fitness_in_gen):
        standard_deviation = 0
        # average fitness of last 4 generations
        avg_fitness = 0
        # sum fitness of last 4 generations
        sum_fitness = 0
        # variance
        variance = 0
        # list of variables for variance
        list_of_fitness = []
        # final value
        coefficient_of_variation = 0
        # check if there are minimum 4 generations
        if self.population.generation > 3:
            for x in range(self.population.generation):
                # sum only last 4 generations
                if x + 4 >= self.population.generation:
                    sum_fitness += best_fitness_in_gen[x]
                    list_of_fitness.append(best_fitness_in_gen[x])
                    # print(list_of_fitness)
                    # print(x, best_fitness_in_gen[x], sum_fitness)
            # arithmetic average
            avg_fitness = sum_fitness / len(list_of_fitness)
            for x in list_of_fitness:
                variance += (x - avg_fitness) * (x - avg_fitness)
            variance = variance / len(list_of_fitness)
            standard_deviation = math.sqrt(variance)
            coefficient_of_variation = standard_deviation / avg_fitness
            self.list_coefficient_of_variation.append(coefficient_of_variation)
            if self.print_logs:
                print(self.population.generation)
                print("Standard deviation:", standard_deviation)
                print("Coefficient of variation:", coefficient_of_variation, "%")
            for x in range(len(self.list_coefficient_of_variation) - 1):
                if (self.list_coefficient_of_variation[x] - self.accuracy < self.list_coefficient_of_variation[x + 1]
                        < self.list_coefficient_of_variation[x] + self.accuracy):
                    return True



    def __print_stats(self):
        print("Generation:", self.population.generation)
        print("Best member's fitness: ", self.population.best_member.fitness)
        print("Best member's operator: ", self.population.best_member.operator.values)
