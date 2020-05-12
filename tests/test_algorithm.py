import unittest
from pyb.src.algorithm import Population


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
        self.population.new_gen()
        self.assertEqual(self.population.generation, 1)

    def test_update_stats(self):
        self.population.update_stats()

    def test_apply_noise(self):
        self.population.apply_noise()
        self.assertEqual(self.population.total_mutations, 10)

    def test_discard_unifit(self):
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 50)


if __name__ == '__main__':
    unittest.main()
