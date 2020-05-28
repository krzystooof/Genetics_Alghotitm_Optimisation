from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config
from pyb.src.algorithm_core import FitnessDifferencesTooSmall


class Algorithm:
    def __init__(self, fitness_callback, variables, population_size=100, accuracy=0.005, rand_low=-100, rand_high=100,
                 reverse=True, noise=0.5, population_discard=0.5, population_chance_bonus=1, crossover_options=None):

        self.population = Population(
            Config(population_size=population_size, num_values=variables, random_low=rand_low, random_high=rand_high,
                   reverse=reverse, population_discard=population_discard, noise=noise,
                   crossover_options=crossover_options, population_chance_bonus=population_chance_bonus))
        self.crossover_options = crossover_options
        self.population_chance_bonus = population_chance_bonus
        self.population_discard = population_discard
        self.noise = noise
        self.reverse = reverse
        self.rand_high = rand_high
        self.rand_low = rand_low
        self.accuracy = accuracy
        self.size = population_size
        self.values = variables
        self.calculate_fitness = fitness_callback
        self.best_fitness_in_gen = []

    def optimise(self):
        while self.population.generation < self.size:
            try:
                self.__calculate_generation_fitness()
            except StopIteration:
                raise
            else:
                self.best_fitness_in_gen.append(self.population.best_member.operator.values[0])
                self.population.update_stats()
                self.__print_stats()
                if self.population.generation > 5 and self.__check_stop_condition(self.best_fitness_in_gen):
                    return self.population.best_member.operator.values
                try:
                    self.population.new_gen()
                except FitnessDifferencesTooSmall:
                    return self.population.best_member.operator.values

    def __calculate_generation_fitness(self):
        for member in self.population.member_list:
            member.fitness = self.calculate_fitness(member.operator.values)

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

    def __print_stats(self):
        print("Generation:", self.population.generation)
        print("Best member's fitness: ", self.population.best_member.fitness)
        print("Best member's operator: ", self.population.best_member.operator.values)
