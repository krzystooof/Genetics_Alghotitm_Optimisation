import pyb
import utime
import gc
from src.port import VCP
from src.port import Inform
from src.algorithm import Population
from src.algorithm import Config


class Main:

    def __init__(self, ):
        """Main function. First to run"""

        # Variables
        self.population = Population(Config())
        self.started = False
        self.initiated = False
        self.is_error = False
        self.test_index = 0
        self.run_time = 0
        # Return the number of bytes of available heap RAM, or -1 if this amount is not known
        self.memory_usage = 0

        # Main loop
        while True:
            # Check for errors
            if self.is_error:
                self.error()

            # Wait for valid data
            self.data = VCP.read()

            while self.data['type'] == 0:  # 0 means no new data
                Inform.waiting()
                pyb.delay(1)
                self.data = VCP.read()  # Reading data
            Inform.running()
            if self.data['type'] == 1:  # desktop client error
                self.error()
            elif self.data['type'] == 2:  # config received
                self.load_config()
            elif self.data['type'] == 3:  # should never appear
                self.error()
            elif self.data['type'] == 4:  # start, stop, pause, restart
                self.control()
            elif self.data['type'] == 9:  # data to feed to population
                self.feed()

            self.run()

    def error(self):
        Inform.error()
        self.is_error = True
        # periodically check for stop
        while self.is_error:
            data = VCP.read()
            try:
                if data['type'] == 4:
                    if data['operation'] == "STOP":
                        self.started = False
                        self.is_error = False
                        Inform.waiting()
            except KeyError:
                print("Unable to read 'type' field from received data")
            pyb.delay(10)

    def load_config(self):
        """Feeds configuration variables into algorithm"""
        try:
            config = Config(population_size=self.data['config']['population_size'],
                            population_discard=self.data['config']['population_discard'],
                            population_chance_bonus=self.data['config']['population_chance_bonus'],
                            noise=self.data['config']['population_noise'],
                            reverse=self.data['config']['population_reverse_fitness'],
                            random_low=self.data['config']['member_config']['random_low'],
                            random_high=self.data['config']['member_config']['random_high'],
                            num_values=self.data['config']['member_config']['num_values'],
                            crossover_options=self.data['config']['member_config']['crossover_options'])
        except KeyError:
            raise KeyError(str(self.data))
        if self.initiated:
            self.population.config = config
        else:
            self.population = Population(config)
            self.initiated = True

    def control(self):
        """Starts, stops, pauses algorithm"""
        if self.data['operation'] == "STOP":
            self.run_time = 0
            self.initiated = False
            self.started = False
        if self.data['operation'] == "PAUSE":
            self.started = False
        if self.data['operation'] == "START":
            self.started = True

    def feed(self):
        self.population.member_list[self.data['index']].fitness = self.data['fitness']

    def run(self):
        if self.started and self.initiated:  # Not paused and population exists
            if self.test_index == self.population.config.population_size - 1:
                # Tested everyone, new gen, test again

                # Start timer
                start = utime.ticks_us()
                gc.collect()
                before = gc.mem_free()
                # Run code
                self.population.new_gen()
                self.test_index = 0

                # Check for break condition
                if self.population.generation > 100:  # TODO remove hardcoded stop condition
                    self.started = False

                # Stop the timer, save the time
                gc.collect()
                after = gc.mem_free()
                stop = utime.ticks_us()
                self.run_time = utime.ticks_diff(stop, start) + self.run_time
                self.memory_usage = after - before + self.memory_usage
                self.send_stats()
            else:
                # Send next for testing
                VCP.attach('type', 9)
                VCP.attach('index', self.test_index)
                VCP.attach('operator', self.population.member_list[self.test_index].operator.values)
                VCP.send()
                self.test_index += 1

    def send_stats(self):
        VCP.attach('type', 2)

        VCP.attach('best_operator', self.population.best_member.operator.values)
        VCP.attach('best_fitness', self.population.best_member.fitness)
        VCP.attach('generation', self.population.generation)
        VCP.attach('mutations', self.population.total_mutations)
        VCP.attach('crossovers', self.population.total_crossovers)
        VCP.attach('discarded', self.population.total_discarded)
        VCP.attach('time_us', self.run_time)
        VCP.attach('memory_usage', self.memory_usage)

        VCP.send()


main = Main()
