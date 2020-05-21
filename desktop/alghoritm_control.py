"""This module contains code used to control the algorithm on board"""
import time

from usb import USB


class Controller:
    """
            Handles controlling PyBoard
            @author: Krzysztof Greczka
        """

    def __init__(self):
        self.usb = USB()
        self.is_running = False

    def stop_algorithm(self):
        self.is_running = False
        self.usb.attach("type", 4)
        operation = "STOP"
        self.usb.attach("operation", operation)
        self.usb.send()


    def start_algorithm(self, generations, population_size, population_discard, population_chance_bonus,
                        population_noise, mutation_options, crossover_options, reverse_fitness, pyboard_port):
        operation = "START"

        config = {
            "generations": generations,
            "population_size": population_size,
            "population_discard": population_discard,
            "population_chance_bonus": population_chance_bonus,
            "population_noise": population_noise,
            "member_mutation_options": mutation_options,
            "member_crossover_options": crossover_options,
            "population_reverse_fitness": reverse_fitness
        }
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
        self.usb.attach("type", 4)
        operation = "PAUSE"
        self.usb.attach("operation", operation)
        self.usb.send()

    def fitness_reply(self):
        while True:
            reply = self.usb.read()
            try:
                if reply and reply['type'] == 9:
                    index = reply['index']
                    operator = reply['operator']
                    # TODO fitness =
                    self.usb.attach("type", 9)
                    self.usb.attach('index', index)
                    # TODO self.usb.attach('fitness', fitness)
                    self.usb.send()
            except KeyError as error:
                raise IOError("Pyboard reply without expected field" + repr(error))
            finally:
                time.sleep(1)