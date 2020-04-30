import random


class Member:
    def __init__(self, raw_input, crossover_method, mutation_method):
        # raw_input - info from STM pins
        self.input  # TODO = parse raw_input to structural input
        self.crossover_method = crossover_method
        self.fitness = 0

    def calculate_fitness(self):
        # TODO
        # calculate fitness
        self.fitness = len(self.input)  # primitive calculating method
        return self.fitness

    def mutate(self, mutation_method):
        # self.input - list
        i = 0
        j = 0
        while j - i < 2:
            i = random.randint(0, len(self.input))
            j = random.randint(i, len(self.input))
        if mutation_method == 1:  # random resetting - set random element to 0
            self.input[i] = 0
        elif mutation_method == 2:  # swap mutation - swap two elements
            self.input[i], self.input[j] = self.input[j], self.input[i]
        elif mutation_method == 3:  # scramble mutation - shuffle random part
            new_list = self.input[i:j]
            random.shuffle(new_list)
            self.input[i:j] = new_list
        elif mutation_method == 4:  # inversion mutation - invert random part
            self.input[i:j] = list(reversed(self.input[i:j]))

    def crossover(self,crossover_method , parent):
        # returns a child
        # self.input - list
        i = 0
        j = 0
        while j - i < 2:
            length = len(self.input)
            if len(parent.input) < length:
                length = len(parent.input)
            i = random.randint(0, length)
            j = random.randint(i, length)
        if crossover_method == 1:  # one point
            return self.input[:i] + parent.input[i:]
        elif crossover_method == 2:  # multi point
            return self.input[:i] + parent.input[i:j] + self.input[j:]
