import unittest
from pyb.src.algorithm import Population
from pyb.src.algorithm import Member
from pyb.src.algorithm import Operator
import random


def get_config():
    """Configuration of Population"""
    mutate = [1, 2, 3, 4]
    crossover = [1, 2]
    config_dict = {
        'population_size': 100,
        'population_discard': 0.5,
        'population_noise': 0.1,
        'population_chance_bonus': 2,
        'population_reverse_fitness': True,
        'population_base_start': -100,
        'population_base_end': 100,
        'member_mutation_options': mutate,
        'member_crossover_options': crossover

    }
    return config_dict


class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.config = get_config()
        self.population = Population(self.config)
        self.member_list = []
        for x in range(0, self.population.population_size):
            self.member_list.append(Member(Operator([random.uniform(-100, 100)])))  # TODO randomize initial values

    """SPRAWDZAC SKRAJNE PRZYPADKI"""

    def test_load_config(self):
        self.population.load_config(self.config)
        self.assertEqual(self.population.population_size, 100)
        self.assertEqual(self.population.population_discard, 0.5)
        self.assertEqual(self.population.noise, 0.1)
        self.assertEqual(self.population.population_chance_bonus, 2)
        self.assertEqual(self.population.reverse, True)
        self.assertEqual(self.population.mutation_options, [1, 2, 3, 4])
        self.assertEqual(self.population.crossover_options, [1, 2])

    def test_new_gen(self):
        """Testing for 1 generation"""
        self.population.new_gen()
        self.assertEqual(self.population.generation, 1)
        """Testing for 1001 generation"""
        for x in range(1000):
            self.population.new_gen()
        self.assertEqual(self.population.generation, 1001)

    def test_sort_by_fitness(self):
        """Need member to test it"""
        self.assertEqual(1, 1)

    def test_discard_unfit(self):
        """Testing for basic values"""
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 50)
        """Testing for values multiplied by 100"""
        self.population.population_discard = self.population.population_discard * 100
        self.population.population_size = self.population.population_size * 100
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 500000)

    def test_breed_to_fill(self):
        self.population.breed_to_fill()
        self.assertEqual(self.population.total_crossovers, 0)

    def test_assign_cross_chances(self):
        """Need member to test"""
        self.population.assign_cross_chances()
        for member in self.population.member_list:
            self.assertEqual(member.crossover_chance, 0.5)



    def test_get_average_fitness(self):
        final_return = self.population.get_average_fitness()
        """Testing member fitness"""
        for member in self.population.member_list:
            self.assertEqual(member.fitness, 0)
        self.assertEqual(len(self.population.member_list), 100)
        self.assertEqual(final_return, 0)

    def test_get_offset(self):
        final_return = self.population.get_offset()
        self.assertEqual(final_return, 1)

    def test_apply_noise(self):
        self.population.apply_noise()
        self.assertEqual(self.population.total_mutations, 10)

    def test_update_stats(self):
        """"""
        self.population.update_stats()
        self.assertEqual(self.population.best_member, self.population.member_list[0])


if __name__ == '__main__':
    unittest.main()
