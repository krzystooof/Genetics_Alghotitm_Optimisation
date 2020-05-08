import ujson
import pyb

from pyb.src.port import VCP
from pyb.src.port import Inform
from pyb.src.algorithm import Population


class Main:

    def __init__(self):
        """Main function. First to run"""
        # Variables
        self.usb = VCP()
        self.population = Population()
        self.started = False
        self.initiated = False
        self.is_error = False

        while True:

            # Wait for valid data
            self.data = self.usb.read()
            while self.data['type'] == 0:
                pyb.delay(10)

            # Reading data
            if self.data['type'] == 1:  # desktop client error
                self.error()
            elif self.data['type'] == 2:  # config received
                self.load_config()
            elif self.data['type'] == 3:  # should never appear
                self.error()
            elif self.data['type'] == 4:  # start, stop, pause, restart
                self.control()
            elif self.data['type'] == 9:  # data to feed to population
                pass

        # Comment here
        population = Population(operator, population_size, population_discard, noise, mutation_options,
                                crossover_options)
        test_population(population)
        best_member = population.get_population_info()
        print("Best result: ", best_member.operator.values)

        # Comment here
        generations_values = []  # List for further saving results to json
        for x in range(0, generations):
            population.new_gen(population)
            test_population(population)
            best_member = population.get_population_info()
            generations_values.append(best_member.operator.values)
            print("Best result: ", best_member.operator.values)

        # Save results
        # TODO: This must be saved but cannot stay in main_pyb.py as its prepared for execution on STM
        results = {f'generation_{counter}': value for counter, value in enumerate(generations_values)}
        with open("../../tests/algorithm_results.json", "w") as outfile:
            ujson.dump(results, outfile, indent=4)

        # Comment here
        usb.attach("best_member_values", best_member.operator.values)
        usb.attach("best_member_fitness", best_member.fitness)

    def error(self):
        Inform.error()
        self.is_error = True
        while self.is_error:
            data = self.usb.read()
            try:
                if data['type'] == 4:
                    if data['operation'] == "STOP":
                        self.started = False
                        self.is_error = False
                    if data['operation'] == "RESTART":
                        self.started = True
                        self.is_error = False
            except KeyError:
                print("Unable to read 'type' field from received data")
            pyb.delay(10)

    def load_config(self):
        if self.initiated:
            self.population.load_config(self.data['config'])
        else:
            self.population = Population(self.data['config'])
            self.initiated = True

    def control(self):
        try:
            if self.data['operation'] == "STOP":
                self.initiated = False
                self.started = False
            if self.data['operation'] == "RESTART":
                self.initiated = False
                self.started = True
            if self.data['operation'] == "PAUSE":
                self.started = False
            if self.data['operation'] == "START":
                self.started = True
        except KeyError:
            print("Unable to read 'operation' field from received data")
            self.is_error = True

    def feed(self):
        pass



def test_population(population):
    """Sends every member of given population for testing on desktop side"""
    # send data to calculate fitness and save reply
    for member in population.member_list:
        usb.attach('operator', member.operator)
        usb.send()
        reply = usb.read()
        while reply["type"] is 0:
            reply = usb.read()
        try:
            member.fitness = reply["fitness"]
        except KeyError:
            # item not in dictionary
            member.fitness = 0


main = Main()