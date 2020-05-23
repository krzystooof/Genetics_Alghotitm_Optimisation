import pyb
import timeit
import gc
from src.port import VCP
from src.port import Inform
from src.algorithm import Population


# Run a garbage collection
gc.collect()
# Return the number of bytes of available heap RAM
gc.mem_free()
# Return the number of bytes of heap RAM that are allocated
gc.mem_alloc()

algorithm_time = 0
start = 0
stop = 0


class Main:

    def __init__(self, ):
        """Main function. First to run"""

        # Variables
        self.usb = VCP()
        self.population = Population(None)
        self.started = False
        self.initiated = False
        self.is_error = False
        self.test_index = 0
        self.run_time = 0

        # Main loop
        while True:
            # Check for errors
            if self.is_error:
                self.error()

            # Wait for valid data
            self.data = self.usb.read()

            while self.data['type'] == 0:  # 0 means no new data
                Inform.waiting()
                pyb.delay(1)
                self.data = self.usb.read()  # Reading data
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
            data = self.usb.read()
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
        if self.initiated:
            self.population.load_config(self.data['config'])
        else:
            self.population = Population(self.data['config'])
            self.initiated = True

    def control(self):
        """Starts, stops, pauses algorithm"""
        if self.data['operation'] == "STOP":
            stop = timeit.default_timer()
            print("Algorithm worked for: ", algorithm_time)
            algorithm_time = 0
            self.initiated = False
            self.started = False
        if self.data['operation'] == "PAUSE":
            stop = timeit.default_timer()
            algorithm_time = stop - start + algorithm_time
            print("Algorithm worked for: ", algorithm_time)
            self.started = False
        if self.data['operation'] == "START":
            start = timeit.default_timer()
            self.started = True

    def feed(self):
        self.population.member_list[self.data['index']].fitness = self.data['fitness']

    def run(self):
        if self.started and self.initiated:  # Not paused and population exists
            if self.test_index == self.population.population_size - 1:
                # Tested everyone, new gen, test again
                start = timeit.default_timer()
                self.population.new_gen()
                self.test_index = 0
                if self.population.generation == self.population.break_generation:
                    self.started = False
                stop = timeit.default_timer()
                self.run_time = stop - start + self.run_time
                algorithm_time = self.run_time + algorithm_time
                self.send_stats()
            else:
                # Send next for testing
                self.usb.attach('type', 9)
                self.usb.attach('index', self.test_index)
                self.usb.attach('operator', self.population.member_list[self.test_index].operator.values)
                self.usb.send()
                self.test_index += 1

    def send_stats(self):
        self.usb.attach('type', 2)
        self.population.update_stats()
        self.usb.attach('best_operator', self.population.best_member.operator.values)
        self.usb.attach('best_fitness', self.population.best_member.fitness)
        self.usb.attach('generation', self.population.generation)
        self.usb.attach('mutations', self.population.total_mutations)
        self.usb.attach('crossovers', self.population.total_crossovers)
        self.usb.attach('discarded', self.population.total_discarded)
        self.usb.attach('time', stop - start)
        self.usb.attach('total_time', self.run_time)
        self.usb.send()


main = Main()

