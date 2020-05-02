import math
import random

from src.member import Member
from src.operator import Operator


def sort_population_by_fitness(population):
    return sorted(population.member_list, key=lambda member: member.fitness)


class Population:

    def __init__(self):  # Create random population
        # Variables to set
        self.operator = Operator([])
        self.population_size = 100
        self.population_discard = 0.0
        self.noise = 0.0
        # 1 - random resetting - set random element to 0, 2 - swap mutation - swap two elements, 3 - scramble
        # mutation - shuffle random part, 4 - inversion mutation - invert random part
        self.mutation_options = []
        # 1 - one point, 2 - multi point
        self.crossover_options = []

        # generations specific variables - don't change
        self.generation = 0
        self.total_mutations = 0
        self.random_fill = 0
        self.best_fitness = 0
        self.member_list = []
        self.members_to_mutate = 0

        # Filling population with random members
        for x in range(0, self.population_size):
            self.member_list.append(Member(self.input, self.operator))

        # Printing info
        self.__print_generation__()

    def new_gen(self, population):  # Create new population by mutating given population
        # Rewriting variables that won't change in new population
        self.population_discard = population.population_discard
        self.population_size = population.population_size
        self.generation = population.generation + 1
        self.mutation_options = population.mutation_options
        self.crossover_options = population.crossover_options
        self.member_list.clear()

        # Calculate fitness
        for member in population.member_list:
            member.calculate_fitness()

        # Calculating total members to discard and first discard index
        discard_members = math.floor(self.population_discard * self.population_size)
        discard_index_start = self.population_size - discard_members

        # Sorting population by fitness
        sorted_list = sort_population_by_fitness(population)

        # Discarding unfit members
        for x in range(discard_index_start, self.population_size):
            sorted_list.pop(x)

        # Calculating total fitness of remaining members
        fitness_sum = 0
        for x in range(0, len(sorted_list)):
            fitness_sum += sorted_list[x].fitness

        # Calculating tickets for each remaining member. One ticket allows member for one "child"
        ticket_list = []
        for x in range(0, len(sorted_list)):
            tickets = sorted_list[x].fitness / fitness_sum
            tickets = math.floor(tickets)
            ticket_list.insert(x, tickets)

        # Rewriting fit members to new population
        self.member_list = sorted_list

        # Adding mutations to new population
        mutations_made = -1
        while mutations_made != 0:
            mutations_made = 0
            for x in range(0, len(sorted_list) - 1):
                # mutations are crossover type
                crossover_type = random.choice(self.crossover_options)
                if ticket_list[x] >= 1 and ticket_list[x + 1] >= 1:
                    self.member_list.append(sorted_list[x].crossover(crossover_type, sorted_list[x + 1]))
                    mutations_made += 1
            self.total_mutations += mutations_made

        # Adding new random members to the list
        self.random_fill = self.population_size - len(self.member_list)
        for x in range(0, self.random_fill):
            self.member_list.append(Member(self.input, self.operator))

        # Adding random noise
        self.members_to_mutate = self.noise * self.population_size
        for x in range(0, math.floor(self.members_to_mutate)):
            index = random.randint(0, self.population_size)
            mutation_type = random.choice(self.mutation_options)
            self.member_list[index].mutate(mutation_type)

        sort_population_by_fitness(self)
        best_member = population.member_list[0]
        self.best_fitness = best_member.fitness

        self.__print_generation__()

        return best_member.operator

    def __print_generation__(self):
        print("==============================")
        print("Generation: ", self.generation)
        print("Population size: ", self.population_size)
        print("Best fitness: ", self.best_fitness)
        print("Total crossovers: ", self.total_mutations)
        print("New random members: ", self.random_fill)
        print("Total random mutations: ", self.members_to_mutate)
