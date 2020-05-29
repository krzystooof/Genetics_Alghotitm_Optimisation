"""This module contains code used to control the algorithm on board"""
import json
import time

from fitness import get_fitness
from usb import USB


def create_config(population_size, population_discard, population_noise,
                  reverse_fitness, random_low, random_high, crossover_options):
    return {
        "population_size": int(population_size),
        "population_discard": float(population_discard),
        "noise": float(population_noise),
        "reverse": bool(reverse_fitness),
        "random_low": int(random_low),
        "random_high": int(random_high),
        "crossover_options": crossover_options
    }


class Controller:
    """
            Handles controlling PyBoard
            @author: Krzysztof Greczka
    """

    def __init__(self):
        self.is_running = False

    def stop_algorithm(self):
        self.is_running = False
        self.usb.attach("type", 4)
        operation = "STOP"
        self.usb.attach("operation", operation)
        self.usb.send()

    def start_algorithm(self, config, pyboard_port):
        operation = "START"
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
        reply = self.usb.read()
        if not reply['type'] == 0:
            try:
                if reply['type'] == 9:
                    operator = reply['operator']
                    fitness = get_fitness(operator)
                    self.usb.attach("type", 9)
                    self.usb.attach('fitness', fitness)
                    self.usb.send()
                    to_ret = "Operator: " + str(operator) + ", returned fitness: " + str(fitness)
                elif reply['type'] == 2:
                    to_ret = "Received generation results: \n" + str(reply)
                    with open("results.txt", "w") as file:
                        json.dump(reply, file)
                elif reply['type'] == 4:
                    to_ret = "Pyboard performed operation: " + reply['operation']
            except KeyError as error:
                raise IOError("Pyboard reply without expected field" + repr(error))
            finally:
                return to_ret
        else:
            time.sleep(0.00001)
