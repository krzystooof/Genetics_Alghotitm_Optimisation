from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config
from pyb.src.algorithm_core import FitnessDifferencesTooSmall


class Algorithm:
    def __init__(self, fitness_callback, num_values, accuracy=0.005, **kwargs):
        self.population = Population(Config(num_values=num_values, **kwargs))
        self.execute_callback = fitness_callback
        self.accuracy = accuracy
        self.best_fitness_in_gen = []

    def optimise(self):
        while self.population.generation < self.population.config.population_size:
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

    def __print_stats(self):
        print("Generation:", self.population.generation)
        print("Best member's fitness: ", self.population.best_member.fitness)
        print("Best member's operator: ", self.population.best_member.operator.values)
