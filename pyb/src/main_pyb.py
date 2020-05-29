import time
import gc
import pyb
from src.port import VCP
from src.port import Inform
from src.algorithm import Algorithm


def ask_via_usb(list_of_values):
    import src.port as port
    port.VCP.attach('operator', list_of_values)
    port.VCP.attach('type', 9)
    port.VCP.send()
    data = port.VCP.read()
    while data['type'] == 0:
        data = port.VCP.read()
    if data['type'] == 9:
        return data['fitness']
    else:
        VCP.pushed_back = data
        raise StopIteration

class Main:

    def __init__(self, ):
        """Main function. First to run"""

        # Variables
        self.algorithm = None
        self.finished = False
        self.is_error = False
        self.current_best = []

        VCP.open()

        # Main loop
        while True:
            # Check for errors
            if self.is_error:
                self.error()

            # Wait for valid data
            self.read_data()

            Inform.running()
            if self.data['type'] == 2:  # config received
                self.load_config()
            elif self.data['type'] == 4:  # start, stop, pause, restart
                self.control()

    def read_data(self):
        self.data = VCP.read()
        delay = 5
        while self.data['type'] == 0:
            if delay < 10000000:  # tenth of a second
                delay = round(delay * 1.5)
            time.sleep_us(delay)
            Inform.waiting()
            self.data = VCP.read()

    def error(self):
        """Flashes red diode and waits for STOP"""
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
        if self.algorithm is None:
            self.algorithm = Algorithm(ask_via_usb,
                                       self.data['config']['num_values'],
                                       self.data['config']['accuracy'],
                                       **self.data['config']['config'])

    def control(self):
        """Starts, stops, pauses algorithm"""
        if self.data['operation'] == "STOP":
            VCP.attach('type', 4)
            VCP.attach('operation', 'STOP')
            VCP.send()
            self.algorithm = None
            self.send_stats()
        elif self.data['operation'] == "PAUSE":
            VCP.attach('type', 4)
            VCP.attach('operation', 'PAUSE')
            VCP.send()
            self.send_stats()
        elif self.data['operation'] == "START":
            VCP.attach('type', 4)
            VCP.attach('operation', 'START')
            VCP.send()
            try:
                self.current_best = self.algorithm.optimise()
                self.send_stats()
                VCP.attach('type', 4)
                VCP.attach('operation', 'STOP')
                VCP.send()
            except StopIteration:
                self.current_best = self.algorithm.population.best_member.operator.values

    def send_stats(self):
        VCP.attach('type', 2)
        VCP.attach('best_operator', self.current_best)
        VCP.attach('generation', self.algorithm.population.generation)
        gc.collect()
        VCP.attach('free_memory', gc.mem_free())
        VCP.attach('alloc_memory', gc.mem_alloc())
        VCP.send()


main = Main()
