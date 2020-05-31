import unittest
from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config


class TestPopulation(unittest.TestCase):
    def setUp(self, **kwargs):
        self.config = Config(kwargs)
        self.population = Population(**kwargs)
        self.member_list = []

    def test_load_config(self):
        # Testing configuration
        self.assertEqual(self.population.config.population_size, 100)
        self.assertEqual(self.population.config.population_discard, 0.5)
        self.assertEqual(self.population.config.noise, 0.5)
        self.assertEqual(self.population.config.population_chance_bonus, 1)
        self.assertEqual(self.population.config.reverse, False)
        self.assertEqual(self.population.config.random_low, -100)
        self.assertEqual(self.population.config.random_high, 100)
        self.assertEqual(self.population.config.num_values, 10)
        self.assertEqual(self.population.config.crossover_options, [1, 2])

    def test_new_gen(self):
        # Testing for 100 generation
        counter = 1
        for x in range(100):
            for member in self.population.member_list:
                member.fitness = counter
                counter += 1
            self.population.new_gen()
        self.assertEqual(self.population.generation, 100)

    def test_sort_by_fitness(self):
        # Give fitness and testing
        counting = 200
        for member in self.population.member_list:
            member.fitness = counting
            counting += 1
        self.population.sort_by_fitness()
        self.assertEqual(self.population.member_list[0].fitness, 299)

    def test_discard_unfit(self):
        # Testing for basic values
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 50)
        # Testing for values multiplied by 100
        self.population.config.population_discard = self.population.config.population_discard * 100
        self.population.config.population_size = self.population.config.population_size * 100
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 500000)

    def test_breed_to_fill(self):
        counter = 1
        for member in self.population.member_list:
            member.fitness = counter
            counter += 1
        self.population.breed_to_fill()
        self.assertEqual(self.population.total_crossovers, 100)

    def test_assign_cross_chances(self):
        # Basic test of method
        counter = 1
        for member in self.population.member_list:
            member.fitness = counter
            counter += 1
        self.population.assign_cross_chances()
        self.assertEqual(self.population.member_list[0].fitness, 100)
        self.assertEqual(self.population.member_list[len(self.member_list) - 1].fitness, 1)

    def test_update_stats(self):
        # Setting fitness and testing method
        counting = 100
        for member in self.population.member_list:
            member.fitness = counting
            counting = counting + 1
        self.population.update_stats()
        self.assertEqual(self.population.best_member.fitness, 199)
