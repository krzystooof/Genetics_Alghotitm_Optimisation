import random

from src.input import Operator


class Member:
    def __init__(self, operator):
        self.fitness = 0
        self.operator = operator

    # calculating outside the code
    def calculate_fitness(self):
        self.fitness = len(self.input)  # primitive calculating method
        return self.fitness

    def mutate(self, mutation_method):
        # self.input - list
        i = 0
        j = 0
        while j - i < 2:
            i = random.randint(0, len(self.operator.values))
            j = random.randint(i, len(self.operator.values))
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

    def crossover(self,crossover_method , parent):
        # returns a child
        # self.operator.values - list
        i = 0
        j = 0
        while j - i < 2:
            length = len(self.operator.values)
            if len(parent.input) < length:
                length = len(parent.operator.values)
            i = random.randint(0, length)
            j = random.randint(i, length)
        if crossover_method == 1:  # one point
            return self.operator.values[:i] + parent.operator.values[i:]
        elif crossover_method == 2:  # multi point
            return self.operator.values[:i] + parent.operator.values[i:j] + self.operator.values[j:]
