""" One such solution to the given problem.

operator - input (see operator class)
"""
import random

from pyb.src.input import Operator


class Member:
    def __init__(self, operator):
        self.fitness = 0
        self.operator = operator

    # calculating outside the code
    def calculate_fitness(self):
        self.fitness = random.randint(5, 10)  # primitive calculating method
        return self.fitness

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
