import math
import random


class Member:
    def get_fitness(self):
        pass


class Population(object):
    member_list = []
    __population_size = 0
    __population_discard = 0.0
    __noise = 0.0
    generation = 0
    total_mutations = 0
    random_fill = 0

    def __init__(self):  # Create random population
        self.__load_population_size()
        self.__load_population_discard()
        self.generation = 0
        for x in range(0, self.__population_size):
            self.member_list.append(Member())

        ## TODO screen info printing
        print("gen 0 created!")

    def __init__(self, population):  # Create new population by mutating given population
        # Rewriting variables that won't change in new population
        self.__population_discard = population.get_population_discard()
        self.__population_discard = population.get_population_size()
        self.generation = population.generation + 1

        # Calculating total members to discard and first discard index
        discard_members = math.floor(self.__population_discard * self.get_population_size())
        discard_index_start = self.__population_size - discard_members

        # Sorting population by fitness
        sorted_list = sorted(population.member_list, key=lambda member: member.get_fitness())

        # Discarding unfit members
        for x in range(discard_index_start, self.__population_size):
            sorted_list.pop(x)

        # Calculating total fitness of remaining members
        fitness_sum = 0
        for x in range(0, len(sorted_list)):
            fitness_sum += sorted_list[x].calculate_fitness()

        # Calculating tickets for each remaining member. One ticket allows member for one "child"
        ticket_list = []
        for x in range(0, len(sorted_list)):
            tickets = sorted_list[x].get_fitness() / fitness_sum
            tickets = math.floor(tickets)
            ticket_list.insert(x, tickets)

        ## TODO print best member fitness

        # Rewriting fit members to new population
        for x in range(0, len(sorted_list)):
            self.member_list.append(sorted_list[x])

        # Adding mutations to new population
        mutations_made = -1
        while mutations_made != 0:
            mutations_made = 0
            for x in range(0, len(sorted_list) - 1):
                # These mutations are crossover type
                if ticket_list[x] >= 1 and ticket_list[x + 1] >= 1:
                    self.member_list.append(sorted_list[x].crossover(sorted_list[x + 1]))
                    mutations_made += 1
            self.total_mutations += mutations_made

        ## TODO print mutations

        # Adding new random members to the list
        self.random_fill = self.__population_size - len(self.member_list)
        for x in range(0, self.random_fill):
            self.member_list.append(Member())

        # Adding random noise
        members_to_mutate = self.__noise * self.__population_size
        for x in range(0, members_to_mutate):
            index = random.randint(0, self.__population_size)
            self.member_list[index].mutate()

        ## TODO screen info printing
        print("new gen")

    def __load_population_size(self):
        self.__population_size = 0

    def __load_population_discard(self):
        self.__population_discard = 0.0

    def __load_randomness(self):
        self.__noise = 0.0

    def get_population_size(self):  # returns total members of population
        return self.__population_size

    def get_population_discard(self):  # returns percentage of discarded members for each population
        return self.__population_discard
