"""
Contains necessary code to run algorithm.
@author: Grzegorz Drozda
@author: Roland Jałoszyński
"""

import math
import time

from src.algorithm_core import Population, FitnessDifferencesTooSmall


class Algorithm:
    """Initializes runnable instance with given parameters.

    Mandatory arguments:
        @param fitness_callback Callback function to calculate fitness
        @param num_values Number of fitness function variables
    Optional parameters:
        @param print_logs Print algorithm runtime metadata
        @param time_function Function responsible for measuring time
        @param population_size - Size of population (Value in range <1:x>)
        @param population_discard Percentage of discarded members with each generation (Value in range <0:1>)
        @param noise Percentage of random mutations for each generation (Value in range <0:1>)
        @param population_chance_bonus Higher values = less accurate crossovers = faster runtime (Value <1-x>)
        @param reverse Tells algorithm which is better: Lower fitness or higher (bool)
        @param random_low Initial values lower limit
        @param random_high Initial values higher limit
        @param member_crossover_options - List of allowed crossover types. Possible values:
            1. One point
            2. Multi point
        @param accuracy - Algorithm accuracy that affects the start of the stop condition
    """

    def __init__(self, fitness_callback, num_values, print_logs=False, accuracy=0.0005, time_function=time.time,
                 **kwargs):
        self.population = Population(num_values=num_values, **kwargs)
        self.execute_callback = fitness_callback
        self.accuracy = accuracy
        self.best_fitness_in_gen = []
        self.print_logs = print_logs
        self.elapsed_time = 0
        self.list_coefficient_of_variation = []
        self.time_function = time_function

    def optimise(self):
        start_timer = self.time_function()
        stop_timer = 0
        while self.population.generation < self.population.config.population_size:
            try:
                stop_timer = self.time_function()
                self.elapsed_time = stop_timer - start_timer
                self.__calculate_generation_fitness()
                start_timer = self.time_function()
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
                    stop_timer = self.time_function()
                    self.elapsed_time = stop_timer - start_timer + self.elapsed_time
                    return self.population.best_member.operator.values

    def __calculate_generation_fitness(self):
        for member in self.population.member_list:
            member.fitness = self.execute_callback(member.operator.values)

    def __check_stop_condition(self, best_fitness_in_gen):
        sum_fitness, variance = 0, 0
        list_of_fitness = []
        # check if there are minimum 4 generations
        if self.population.generation > 3:
            for x in range(self.population.generation):
                # sum only last 4 generations
                if x + 4 >= self.population.generation:
                    sum_fitness += best_fitness_in_gen[x]
                    list_of_fitness.append(best_fitness_in_gen[x])
            # arithmetic average
            avg_fitness = sum_fitness / len(list_of_fitness)
            for x in list_of_fitness:
                variance += (x - avg_fitness) * (x - avg_fitness)
            variance = variance / len(list_of_fitness)
            standard_deviation = math.sqrt(variance)
            coefficient_of_variation = standard_deviation / avg_fitness
            self.list_coefficient_of_variation.append(coefficient_of_variation)
            if self.print_logs:
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
