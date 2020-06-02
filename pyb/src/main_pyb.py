"""Main class for pyboard"""
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
        self.current_best = []

        VCP.open()

        # Main loop
        while True:
            # Check for errors

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
            if delay < 100000:  # tenth of a second
                delay = round(delay * 1.5)
            time.sleep_us(delay)
            Inform.waiting()
            self.data = VCP.read()

    def load_config(self):
        """Feeds configuration variables into algorithm"""
        if self.algorithm is None:
            self.algorithm = Algorithm(ask_via_usb,
                                       num_values=self.data['config']['num_values'],
                                       log=False,
                                       accuracy=self.data['config']['accuracy'],
                                       time_function=time.ticks_us,
                                       **self.data['config']['config'])

    def control(self):
        """Starts, stops, pauses algorithm"""
        if self.data['operation'] == "STOP":
            VCP.attach('type', 4)
            VCP.attach('operation', 'STOP')
            VCP.send()
            self.send_stats()
            self.algorithm = None
            gc.collect()
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
                self.algorithm = None
                gc.collect()
                VCP.attach('type', 4)
                VCP.attach('operation', 'STOP')
                VCP.send()
            except StopIteration:
                self.current_best = self.algorithm.population.best_member.operator.values

    def send_stats(self):
        VCP.attach('type', 2)
        if self.algorithm is not None:
            VCP.attach('best_operator', self.current_best)
            VCP.attach('generation', self.algorithm.population.generation)
            VCP.attach('total_time', self.algorithm.elapsed_time)
        gc.collect()
        VCP.attach('free_memory', gc.mem_free())
        VCP.attach('alloc_memory', gc.mem_alloc())
        VCP.send()


main = Main()
