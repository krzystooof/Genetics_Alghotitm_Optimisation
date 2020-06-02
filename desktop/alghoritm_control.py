"""
This module contains code used to control the algorithm on board
@author Krzysztof Greczka
"""

from fitness import get_fitness
from usb import USB




def create_config(num_values, accuracy, population_size, population_discard, population_noise,
                  reverse_fitness, random_low, random_high, crossover_options):
    """
    Creates board readable communicate with given parameters
    """
    config = {
        "population_size": int(population_size),
        "population_discard": float(population_discard),
        "noise": float(population_noise),
        "reverse": bool(reverse_fitness),
        "random_low": float(random_low),
        "random_high": float(random_high),
        "crossover_options": crossover_options
    }
    return {
        "num_values": int(num_values),
        "accuracy": float(accuracy),
        "config": config
    }


class Controller:
    """
            Handles Board controlling and communication
            @author: Krzysztof Greczka
    """

    def __init__(self):
        self.is_running = False



    def stop_algorithm(self):
        """
        Send STOP command
        """
        self.is_running = False
        self.usb.attach("type", 4)
        operation = "STOP"
        self.usb.attach("operation", operation)
        self.usb.send()



    def start_algorithm(self, config, pyboard_port, recreate_usb=True):
        """
        Connect with board using usb, send config and START command
        @param config: board readable communicate with required parameters
        @param pyboard_port: `board communciation USB port
        @param recreate_usb: if False usb is not initialized (when unpausing)
        """
        operation = "START"
        print(recreate_usb)
        if recreate_usb:
            pyboard_port = pyboard_port
            if len(pyboard_port) != 0:
                self.usb = USB(pyboard_port)
            else:
                self.usb = USB()
                pyboard_port = "/dev/ttyACM1 (default Linux PyBoard port)"
        self.usb.attach("type", 2)
        self.usb.attach("config", config)
        self.usb.send()
        self.usb.attach("type", 4)
        self.usb.attach("operation", operation)
        self.usb.send()
        self.is_running = True
        return pyboard_port



    def pause_algorithm(self):
        """
            Send PAUSE command
        """
        self.usb.attach("type", 4)
        operation = "PAUSE"
        self.usb.attach("operation", operation)
        self.usb.send()

    def board_reply(self):
        """
       Function handling board replies and requests
       """
        reply = self.usb.read()
        type = reply['type']
        if type != 0:
            try:
                if type == 9:
                    operator = reply['operator']
                    fitness = get_fitness(operator)
                    self.usb.attach("type", 9)
                    self.usb.attach('fitness', fitness)
                    self.usb.send()
                    to_ret = {"type": 9,
                              "operator": operator,
                              "fitness": fitness}
                elif type == 2 or type == 4:
                    to_ret = reply
            except KeyError as error:
                raise IOError("Pyboard reply without expected field" + repr(error))
            finally:
                return to_ret
