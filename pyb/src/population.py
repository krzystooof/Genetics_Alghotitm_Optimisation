import math
import random

from pyb.src.member import Member

def sort_population_by_fitness(population):
    return sorted(population.member_list, key=lambda member: member.fitness)


class Population:

    def __init__(self, operator, population_size, population_discard, noise, mutation_options,
                 crossover_options):  # Create random population
        # Variables to set
        self.operator = operator
        self.population_size = population_size
        self.population_discard = population_discard
        self.noise = noise
        # 1 - random resetting - set random element to 0, 2 - swap mutation - swap two elements, 3 - scramble
        # mutation - shuffle random part, 4 - inversion mutation - invert random part
        self.mutation_options = mutation_options
        # 1 - one point, 2 - multi point
        self.crossover_options = crossover_options

        # generations specific variables - don't change
        self.generation = 0
        self.total_crossovers = 0
        self.random_fill = 0
        self.best_fitness = 0
        self.member_list = []
        self.members_to_mutate = 0

        # Filling population with random members
        for x in range(0, self.population_size):
            self.member_list.append(Member(self.operator))

        # TODO method to get fitness from outside
        # calculate fitness
        for member in self.member_list:
            member.calculate_fitness()

        # Printing info
        self.__print_generation__()

    def new_gen(self, population):  # Create new population by mutating given population
        # Rewriting variables that won't change in new population
        self.population_discard = population.population_discard
        self.population_size = population.population_size
        self.generation = population.generation + 1
        self.mutation_options = population.mutation_options
        self.crossover_options = population.crossover_options

        # Calculating total members to discard and first discard index
        discard_members = math.floor(self.population_discard * self.population_size)
        discard_index_start = self.population_size - discard_members - 1

        # Sorting population by fitness
        sorted_list = sort_population_by_fitness(population)

        # Discarding unfit members
        for x in range(self.population_size, discard_index_start):
            sorted_list.pop(x)

        # Calculating total fitness of remaining members
        fitness_sum = 0
        for x in range(0, len(sorted_list)):
            fitness_sum += sorted_list[x].fitness

        # Calculating tickets for each remaining member. One ticket allows member for one "child"
        ticket_list = []
        for x in range(0, len(sorted_list)):
            tickets = sorted_list[x].fitness / fitness_sum
            tickets = int(tickets)
            ticket_list.insert(x, tickets)

        # Rewriting fit members to new population
        # TODO remove non fit members
        self.member_list = sorted_list
        self.population_size = len(self.member_list)

        # Adding mutations to new population

        crossovers_made = 0
        for x in range(0, len(ticket_list) - 1):
            for y in range(0, len(ticket_list) - 1):
                # mutations are crossover type
                crossover_type = random.choice(self.crossover_options)
                if ticket_list[x] >= 1 and ticket_list[y] >= 1:
                    self.member_list.append(self.member_list[x].crossover(crossover_type, self.member_list[y]))
                    crossovers_made += 1
        self.total_crossovers += crossovers_made

        self.population_size = len(self.member_list)

        # Adding new random members to the list
        self.random_fill = self.population_size - len(self.member_list)
        for x in range(0, self.random_fill):
            self.member_list.append(Member(self.operator))

        self.population_size = len(self.member_list)

        # Adding random noise
        self.members_to_mutate = self.noise * self.population_size
        for x in range(0, math.floor(self.members_to_mutate)):
            index = random.randint(0, self.population_size - 1)
            mutation_type = random.choice(self.mutation_options)
            self.member_list[index].mutate(mutation_type)

        self.population_size = len(self.member_list)

        # TODO method to get fitness from outside
        # calculate fitness
        for member in self.member_list:
            member.calculate_fitness()

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
        print("Total crossovers: ", self.total_crossovers)
        print("New random members: ", self.random_fill)
        print("Total random mutations: ", self.members_to_mutate)
