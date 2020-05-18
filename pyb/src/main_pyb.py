import pyb

from src.port import VCP
from src.port import Inform
from src.algorithm import Population


class Main:

    def __init__(self, ):
        """Main function. First to run"""

        # Variables
        self.usb = VCP()
        self.population = Population({})
        self.started = False
        self.initiated = False
        self.is_error = False
        self.test_index = 0

        # Main loop
        while True:
            # Check for errors
            if self.is_error:
                self.error()

            # Wait for valid data
            Inform.waiting()
            self.data = self.usb.read()
            try:
                while self.data['type'] == 0:  # 0 means no new data
                    pyb.delay(10)
                    self.data = self.usb.read()

                # Reading data
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
            except KeyError:
                print("Incomplete data")
                self.is_error = True

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
        # TODO load generations number
        # I dont remember what i meant by this ^^^
        # Dont worry. I will once something breaks.
        if self.initiated:
            self.population.load_config(self.data['config'])
        else:
            self.population = Population(self.data['config'])
            self.initiated = True

    def control(self):
        """Starts, stops, pauses algorithm"""
        if self.data['operation'] == "STOP":
            self.initiated = False
            self.started = False
        if self.data['operation'] == "PAUSE":
            self.started = False
        if self.data['operation'] == "START":
            self.started = True

    def feed(self):
        self.population.member_list[self.data['index']].fitness = self.data['fitness']

    def run(self):
        if self.started and self.initiated: # Not paused and population exists
            if self.test_index == self.population.population_size - 1:
                # Tested everyone, new gen, test again
                self.population.new_gen()
                self.test_index = 0
            else:
                # Send next for testing
                self.usb.attach('index', self.test_index)
                self.usb.attach('operator', self.population.member_list[self.test_index].operator)
                self.test_index += 1


main = Main()
