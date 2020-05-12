"""This module contains code used to control the algorithm on board"""
from desktop.usb import USB


class Controller:
    """
            Handles controlling PyBoard
            @author: Krzysztof Greczka
        """

    def __init__(self, gui, checkboxes_one_set):
        self.checkboxes_one_set = checkboxes_one_set
        self.gui = gui
        self.usb = USB()

    def stop_algorithm(self):
        self.gui.disable_buttons([0, 1, 2, 3])
        self.gui.log("Stopping")
        self.usb.attach("type", 4)
        operation = "STOP"
        self.usb.attach("operation", operation)
        self.usb.send()
        self.gui.enable_entry(0)
        self.gui.enable_button(0)

    def restart_algorithm(self):
        self.stop_algorithm()
        self.start_algorithm()

    def start_algorithm(self):
        self.gui.disable_buttons([0, 1, 2, 3])
        self.gui.log("Starting")
        try:
            self.gui.check_values(self.checkboxes_one_set)
        except ValueError as error:
            print(repr(error))
            self.gui.log_error(str(error))
            self.gui.log("Start aborted")
            self.gui.enable_buttons([0, 1, 2, 3])
            return
        operation = "START"
        generations = self.gui.get_entry_value(1)
        population_chance_bonus = self.gui.get_entry_value(5)
        population_size = self.gui.get_entry_value(2)
        population_noise = self.gui.get_entry_value(4)
        population_discard = self.gui.get_entry_value(3)
        reverse_fitness = self.gui.get_checkbox_value(6, 0)

        mutation_options = []

        for x, boolean in enumerate(self.gui.get_checkbox_values(7)):
            if boolean.get() is True:
                mutation_options.append(x + 1)
            x += 1

        crossover_options = []

        for x, boolean in enumerate(self.gui.get_checkbox_values(8)):
            if boolean.get() is True:
                crossover_options.append(x + 1)
            x += 1
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
        pyboard_port = self.gui.get_entry_value(0)
        if len(pyboard_port) != 0:
            self.usb = USB(pyboard_port)
        else:
            self.usb = USB()
            pyboard_port = "/dev/ttyACM1 (default Linux PyBoard port)"
        self.gui.log_info("PyBoard port is set to " + pyboard_port)
        self.usb.attach("type", 2)
        self.usb.attach("config", config)
        self.usb.send()
        self.usb.attach("type", 4)
        self.usb.attach("operation", operation)
        self.usb.send()
        self.gui.enable_entry(0)
        self.gui.enable_buttons([1, 2, 3])

    def pause_algorithm(self):
        self.gui.disable_buttons([0, 1, 2, 3])
        self.gui.log("Pausing")
        self.usb.attach("type", 4)
        operation = "PAUSE"
        self.usb.attach("operation", operation)
        self.usb.send()
        self.gui.enable_buttons([1, 2, 3])
        # TODO implement second click to resume
