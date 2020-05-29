"""This module contains code used to control the algorithm on board"""
import json
import time

from fitness import get_fitness
from usb import USB


def create_member_config(random_low, random_high, num_values, crossover_options):
    for x in range(0, len(crossover_options)):
        crossover_options[x] = int(crossover_options[x])
    return {
        "random_low": float(random_low),
        "random_high": float(random_high),
        "num_values": int(num_values),
        "crossover_options": crossover_options
    }


def create_config(population_size, population_discard, population_chance_bonus, population_noise,
                  reverse_fitness, member_config):
    return {
        # This is read by load_config in main_pyb.py. Needs to be compatible on both sides
        "population_size": int(population_size),
        "population_discard": float(population_discard),
        "population_chance_bonus": float(population_chance_bonus),
        "population_noise": float(population_noise),
        "population_reverse_fitness": bool(reverse_fitness),
        "member_config": member_config
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

    def start_algorithm(self, config, pyboard_port, recreate_usb=True):
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
        self.usb.attach("type", 4)
        operation = "PAUSE"
        self.usb.attach("operation", operation)
        self.usb.send()

    def fitness_reply(self):
        reply = self.usb.read()
        if reply:
            try:
                if reply['type'] == 9:
                    index = reply['index']
                    operator = reply['operator']
                    fitness = get_fitness(operator)
                    self.usb.attach("type", 9)
                    self.usb.attach('index', index)
                    self.usb.attach('fitness', fitness)
                    self.usb.send()
                    to_ret = "Operator: " + str(operator) + ", returned fitness: " + str(fitness)
                elif reply['type'] == 2:
                    to_ret = "Received generation results: \n" + str(reply)
                    with open("results.txt", "w") as file:
                        json.dump(reply, file)
            except KeyError as error:
                raise IOError("Pyboard reply without expected field" + repr(error))
            finally:
                return to_ret
        else:
            time.sleep(0.1)
