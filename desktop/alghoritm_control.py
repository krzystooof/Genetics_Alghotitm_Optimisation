"""This module contains code used to control the algorithm on board"""


def stop_algorithm(gui, usb):
    gui.log("Stopping")
    operation = "STOP"
    usb.attach("operation", operation)
    usb.send()


def restart_algorithm(gui, usb):
    gui.log("Restarting")
    stop_algorithm(gui, usb)
    start_algorithm(gui, usb)


def start_algorithm(gui, usb):
    gui.log("Starting")
    try:
        gui.check_values()
    except ValueError as error:
        print(repr(error))
        gui.log_error(str(error))
        gui.log("Start aborted")
        return
    operation = "START"
    generations = gui.generations_spinbox.get()
    population_chance_bonus = gui.population_chance_bonus_spinbox.get()
    population_size = gui.population_size_spinbox.get()
    population_noise = gui.population_noise_spinbox.get()
    population_discard = gui.population_discard_spinbox.get()

    mutation_options = []

    for x, boolean in enumerate(gui.mutation_states):
        if boolean.get() is True:
            mutation_options.append(x + 1)
        x += 1

    crossover_options = []

    for x, boolean in enumerate(gui.crossover_states):
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
        "member_crossover_options": crossover_options
    }
    usb.attach("operation", operation)
    usb.attach("config", config)
    usb.send()


def pause_algorithm(gui, usb):
    gui.log("Stopping")
    operation = "PAUSE"
    usb.attach("operation", operation)
    usb.send()
