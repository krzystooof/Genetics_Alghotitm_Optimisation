from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config
from pyb.src.algorithm_core import FitnessDifferencesTooSmall
import math
import time


class Algorithm:
    def __init__(self, fitness_callback, num_values, log=False, accuracy=0.005, **kwargs):
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
        """
        self.population = Population(num_values=num_values, **kwargs)
        self.execute_callback = fitness_callback
        self.accuracy = accuracy
        self.best_fitness_in_gen = []
        self.print_logs = log
        #time of algorithm
        self.time = 0

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
                self.__check_stop_condition1(self.best_fitness_in_gen)
                self.population.update_stats()
                if self.print_logs:
                    self.__print_stats()
                # if self.population.generation > 5 and self.__check_stop_condition(self.best_fitness_in_gen):
                #     return self.population.best_member.operator.values
                try:
                    self.population.new_gen()
                except FitnessDifferencesTooSmall:
                    stop_timer = time.time()
                    self.time = stop_timer-start_timer + self.time
                    return self.population.best_member.operator.values

    def __calculate_generation_fitness(self):
        for member in self.population.member_list:
            member.fitness = self.execute_callback(member.operator.values)

    def __check_stop_condition(self, best_fitness_in_gen):
        # Sum of fitness of last 5 generations
        sum_of_fitness = 0
        newest_fitness = 0
        for x in range(self.population.generation):
            if self.population.generation - 5 <= x < self.population.generation:
                sum_of_fitness = best_fitness_in_gen[x] + sum_of_fitness
            newest_fitness = best_fitness_in_gen[self.population.generation - 1]
        avg_fitness = sum_of_fitness / 5

        return newest_fitness - self.accuracy < avg_fitness < newest_fitness + self.accuracy

    # using standard deviation
    def __check_stop_condition1(self, best_fitness_in_gen):
        #
        standard_deviation = 0
        # average fitness of last 3 generations
        avg_fitness = 0
        # sum fitness of last 3 generations
        sum_fitness = 0
        # variance
        variance = 0
        # list of variables for variance
        list_of_fitness = []
        # final value
        coefficient_of_variation = 0
        # check if there are minimum 3 generations
        if self.population.generation > 2:
            for x in range(self.population.generation): # 3
                # sum only last 3 generations
                if x+3 >= self.population.generation:
                    sum_fitness += best_fitness_in_gen[x]
                    list_of_fitness.append(best_fitness_in_gen[x])
                    # print(list_of_fitness)
                    # print(x, best_fitness_in_gen[x], sum_fitness)
            # arithmetic average
            avg_fitness = sum_fitness / list_of_fitness.__sizeof__()
            for x in list_of_fitness:
                variance += (x - avg_fitness)*(x - avg_fitness)
            variance = variance / list_of_fitness.__sizeof__()
            standard_deviation = math.sqrt(variance)
            coefficient_of_variation = standard_deviation/avg_fitness
            print(self.population.generation)
            print("Odchylenie standardowe", standard_deviation)
            print("Wspolczynnik zmiennosci", coefficient_of_variation, "%")
            #a) Zrobic accuracy do wspolczynnika zmiennosci czyli jezeli bedzie roznica 0.00001 to konczy
            #b) Zrobic accuracy do odchylenia standardowego czyli jezeli bedzie roznica 0.00001 to konczy





    def __print_stats(self):
        print("Generation:", self.population.generation)
        print("Best member's fitness: ", self.population.best_member.fitness)
        print("Best member's operator: ", self.population.best_member.operator.values)
