from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config

list = []
def celnosc(Population, accuracy, counter):

    return 0

class Algorithm:
    def __init__(self, function_type,
                 values,
                 population,
                 accuracy,
                 rand_low,
                 rand_high,
                 reverse):
        self.result = 0
        self.is_finished = None
        self.reverse = reverse
        self.rand_high = rand_high
        self.rand_low = rand_low
        self.accuracy = accuracy
        self.population = population
        self.values = values
        self.function_type = function_type

        self.counter = 0

    def run(self):
        population = Population(Config(population_size=self.population, num_values=self.values, random_low=self.rand_low, random_high=self.rand_high, reverse=self.reverse))
        for member in population.member_list:
            member.fitness = self.function_type(member.operator.values)
        while population.generation < 100:  # TODO break condition dependent on accuarcy
            population.new_gen()


            for member in population.member_list:
                member.fitness = self.function_type(member.operator.values)

            population.update_stats()
            print("Best member's fitness: ", population.best_member.fitness)
            print("Best member's operator: ", population.best_member.operator.values)
            list.append(population.best_member.operator.values[0])
            if population.generation > 5:
                self.counter = self.counter + 1
                sum = 0
                value_of_the_newest_generation = 0
                # print("Counter:", self.counter)
                # print("pop_gen", population.generation)
                for x in range(population.generation):
                    if x >= self.counter and population.generation > x:
                        sum = list[x] + sum
                    value_of_the_newest_generation = list[x]
                sum = sum / 5
                print(value_of_the_newest_generation)
                if(value_of_the_newest_generation-self.accuracy<sum<value_of_the_newest_generation+self.accuracy):
                    self.is_finished = True
                    self.result = population.best_member.operator.values[0]
                    return
            print("Generation:", population.generation)


        if self.function_type == StopIteration:
            self.is_finished = False
            return
        else:
            self.result = self.function_type(self.result)

