import unittest
from pyb.src.algorithm import Population
from pyb.src.algorithm import Config


def get_config():
    return Config()  # TODO make config work


class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.config = get_config()
        self.population = Population(self.config)
        self.member_list = []

    def test_load_config(self):  # TODO make config testing work or delete this
        """Testing configuration"""
        self.population.load_config(self.config)
        self.assertEqual(self.population.population_size, 100)
        self.assertEqual(self.population.population_discard, 0.5)
        self.assertEqual(self.population.noise, 0.1)
        self.assertEqual(self.population.population_chance_bonus, 2)
        self.assertEqual(self.population.reverse, True)
        self.assertEqual(self.population.member_config["random_low"], -100)
        self.assertEqual(self.population.member_config["random_high"], 100)
        self.assertEqual(self.population.member_config["num_values"], 1)
        self.assertEqual(self.population.member_config["mutation_options"], [1, 2, 3, 4])
        self.assertEqual(self.population.member_config["crossover_options"], [1, 2])

    def test_new_gen(self):
        """Testing for 1 generation"""
        self.population.new_gen()
        self.assertEqual(self.population.generation, 1)
        # Testing for 1001 generation
        for x in range(1000):
            self.population.new_gen()
        self.assertEqual(self.population.generation, 1001)

    def test_sort_by_fitness(self):
        """Give fitness and testing"""
        counting = 200
        for member in self.population.member_list:
            member.fitness = counting
            counting -= 1
        self.population.sort_by_fitness()
        self.assertEqual(self.population.member_list[0].fitness, 101)

    def test_discard_unfit(self):
        """Testing for basic values"""
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 50)
        # Testing for values multiplied by 100
        self.population.population_discard = self.population.population_discard * 100
        self.population.population_size = self.population.population_size * 100
        self.population.discard_unfit()
        self.assertEqual(self.population.total_discarded, 500000)

    def test_breed_to_fill(self):
        self.population.breed_to_fill()
        self.assertEqual(self.population.total_crossovers, 0)

    def test_assign_cross_chances(self):
        """ Basic test of method"""
        self.population.assign_cross_chances()
        for member in self.population.member_list:
            self.assertEqual(member.crossover_chance, 0.5)
        # Testing when member fitness is 2
        for member in self.population.member_list:
            member.fitness = 2
        self.population.assign_cross_chances()
        self.assertEqual(self.population.member_list[0].crossover_chance, 0.5)

    def test_get_average_fitness(self): # TODO nonexistant functions dont need testing
        """Every member has 1 fitness and there are 100 members"""
        for member in self.population.member_list:
            member.fitness = 1
            self.assertEqual(member.fitness, 1)
        final_return = self.population.get_average_fitness()
        self.assertEqual(len(self.population.member_list), 100)
        self.assertEqual(final_return, 1)

    def test_get_offset(self):  # TODO nonexistant functions dont need testing
        """Basic test"""
        final_return = self.population.get_offset()
        self.assertEqual(final_return, 1)
        # Test when first member fitness will be 10000
        self.population.member_list[0].fitness = 10000
        final_return = self.population.get_offset()
        self.assertEqual(final_return, -9999)

    def test_apply_noise(self): # TODO nonexistant functions dont need testing
        """Test of basic values"""
        self.population.apply_noise()
        self.assertEqual(self.population.total_mutations, 10)
        # Test when noise is 100 and population size is 93
        self.population.noise = 100
        self.population.population_size = 93
        self.population.apply_noise()
        self.assertEqual(self.population.total_mutations, 9300)

    def test_update_stats(self):
        """Setting fitness and testing method"""
        counting = 100
        for member in self.population.member_list:
            member.fitness = counting
            counting = counting - 1
        self.population.update_stats()
        self.assertEqual(self.population.best_member.fitness, 1)