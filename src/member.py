import random


class Member:
    def __init__(self, id, raw_input):
        self.id = id
        # raw_input - info from STM pins
        self.input  # = parse raw_input to structural input

    def calculate_fitness(self):
        pass
        # calculate fitness
        # self.fitness = calculated fitness
        # return self.fitness

    def mutate(self, operator):
        # self.input - list
        i = 0
        j = 0
        while j - i < 2:
            i = random.randint(0, len(self.input))
            j = random.randint(i, len(self.input))
        if operator == 1:  # random resetting - set random element to 0
            self.input[i] = 0
        elif operator == 2:  # swap mutation - swap two elements
            self.input[i], self.input[j] = self.input[j], self.input[i]
        elif operator == 3:  # scramble mutation - shuffle random part
            new_list = self.input[i:j]
            random.shuffle(new_list)
            self.input[i:j] = new_list
        elif operator == 4:  # inversion mutation - invert random part
            self.input[i:j] = list(reversed(self.input[i:j]))

    def crossover(self, operator, parent):
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
        if operator == 1:  # one point
            return self.input[:i] + parent.input[i:]
        elif operator == 2:  # multi point
            return self.input[:i] + parent.input[i:j] + self.input[j:]
