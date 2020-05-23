from multiprocessing import Process
from tkinter import END

import serial

from graph import Graph
from gui import GUI
from alghoritm_control import *

p2 = None


def start_button_action(controller, gui, checkboxes_one_set):
    gui.disable_buttons([0, 1, 2, 3])
    gui.log("Starting")
    try:
        gui.check_values(checkboxes_one_set)
    except ValueError as error:
        print(repr(error))
        gui.log_error(str(error))
        gui.log("Start aborted")
        gui.enable_buttons([0, 1, 2, 3])
        return
    generations = gui.get_entry_value(1)
    population_chance_bonus = gui.get_entry_value(5)
    population_size = gui.get_entry_value(2)
    population_noise = gui.get_entry_value(4)
    population_discard = gui.get_entry_value(3)
    reverse_fitness = gui.get_checkbox_value(6, 0)
    pyboard_port = gui.get_entry_value(0)
    random_low = gui.get_entry_value(9)
    random_high = gui.get_entry_value(10)
    num_values = gui.get_entry_value(11)
    mutation_options = []

    for x, boolean in enumerate(gui.get_checkbox_values(7)):
        if boolean.get() is True:
            mutation_options.append(x + 1)
        x += 1

    crossover_options = []

    for x, boolean in enumerate(gui.get_checkbox_values(8)):
        if boolean.get() is True:
            crossover_options.append(x + 1)
        x += 1

    member_config = create_member_config(random_low, random_high, num_values, mutation_options, crossover_options)
    config = create_config(generations, population_size, population_discard, population_chance_bonus, population_noise, reverse_fitness, member_config)

    try:
        pyboard_port = controller.start_algorithm(config, pyboard_port)
        gui.log_info("PyBoard port is set to " + pyboard_port)
        global p2
        p2 = Process(target=lambda: controller.fitness_reply())
        p2.start()
        gui.enable_buttons([1, 2, 3])
    except serial.serialutil.SerialException:
        gui.log_error("Failed connection to board")
        gui.log("Start aborted")
        gui.enable_button(0)
    finally:
        gui.enable_entry(0)



def pause_button_action(controller, gui):
    gui.disable_buttons([0, 1, 2, 3])
    gui.log("Pausing")
    controller.pause_algorithm()
    gui.enable_buttons([0, 1, 2])


def stop_button_action(controller, gui):
    global p2
    p2.terminate()
    gui.disable_buttons([0, 1, 2, 3])
    gui.log("Stopping")
    # TODO add operator to listbox0
    # TODO add time to listbox1
    controller.stop_algorithm()
    gui.enable_entry(0)
    gui.enable_button(0)


def restart_button_action(controller, gui, checkboxes_one_set):
    stop_button_action(controller, gui)
    gui.draw_graph()
    start_button_action(controller, gui, checkboxes_one_set)


def draw_graph_button_action(gui):
    graph = Graph("Time (function)", "function", "time", gui.listboxes[0].get(0, END))
    graph.add_y_axis_data("", gui.listboxes[1].get(0, END), 'lines+markers')
    graph.show()


def debug_button_action(controller, gui):
    gui.log(controller.usb.read_debug())


if __name__ == '__main__':
    gui = GUI("Desktop STM GA Control Panel",10)

    gui.add_text_entry("PyBoard port:")
    gui.add_spinbox("Generations:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Population size:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Population discard:", 0, 1, '%0.3f', 0.001)
    gui.add_spinbox("Population noise:", 0, 1, '%0.3f', 0.001)
    gui.add_spinbox("Population chance bonus::", 1, 9999, '%1.3f', 0.001)

    gui.add_checkboxes("Population reverse fitness:", [""], False)
    gui.add_checkboxes("Member mutation options:", ["Random resetting", "Swap", "Scramble", "Inversion"], False)
    gui.add_checkboxes("Member crossover options:", ["One point", "Multi point"], False)
    # rows with checkboxes that must have at least one option set
    checkboxes_one_set = [7, 8]

    gui.add_spinbox("Member min random:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Member max random:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Number of operator values:", 0, 100, '%1.f', 1)

    gui.add_console()
    gui.log("Fitness caclulating function is located in fintess.py")
    gui.log("Please edit this function before running GUI")

    controller = Controller()

    gui.add_button("START", lambda: start_button_action(controller, gui, checkboxes_one_set))
    gui.add_button("STOP", lambda: stop_button_action(controller, gui))
    gui.add_button("RESTART", lambda: restart_button_action(controller, gui, checkboxes_one_set))
    gui.add_button("PAUSE", lambda: pause_button_action(controller, gui))
    gui.add_button("DRAW GRAPH", lambda: draw_graph_button_action(gui))
    gui.add_button("DEBUG", lambda: debug_button_action(controller, gui))
    gui.disable_buttons([1, 2, 3])

    gui.add_listbox()
    gui.add_listbox()
    p1 = Process(target=gui.work)
    p1.start()
