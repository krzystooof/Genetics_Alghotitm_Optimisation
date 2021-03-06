"""
Main desktop file handling interactions with user. Getting parameters, sending and receiving board communicates,
displaying connection, progress info and drawing graphs.

@author Krzysztof Greczka
"""
import threading
import time

import serial

from graph import Graph
from gui import GUI
from alghoritm_control import *

run_number = 1
full_times = []
full_memory_usage = []
parameter_per_cycle = []
paused = False
last_result = None

reply_thread = None


def board_reply(controller, gui):
    """
    Function handling board replies with fitness requests or alghoritm summary

    @param controller: used to communicate with board
    @param gui: used to display results
    """
    thread = threading.current_thread()
    delay_ms = 5
    while getattr(thread, "do_run", True):
        result = controller.board_reply()
        if result is not None:
            delay_ms = 5
            type = result['type']
            if type == 9:
                operator = str(result['operator'])
                fitness = str(result['fitness'])
                print("Received operator: " + operator + ", sent fitness: " + fitness)
            elif type == 2:
                global last_result
                last_result = result
                gui.log("Received results:\n" + str(result))
            elif type == 4:
                print("Pyboard performed: " + result['operation'])
                if result['operation'] == "STOP":
                    stop_button_action(controller, gui, send_stop=False)
        else:
            if delay_ms < 300000:  # tenth of a second
                delay_ms = round(delay_ms * 1.5)
                delay_s = delay_ms * 0.000001
            time.sleep(delay_s)


def start_button_action(controller, gui, checkboxes_one_set):
    """
    Function handling algorithm starting

    Disable gui buttons for working time, connect with board, get configuration from gui entries and send it to board with 
    starting command. Additional save selected parameter for further displaying (listboxes and graphs)

    @param controller: used to communicate with board
    @param gui: used to display results
    @param checkboxes_one_set: rows with gui checkboxes that at least one option must be selected
    """
    gui.disable_buttons([0, 1, 2, 3])
    gui.log("Starting")
    try:
        gui.check_values(checkboxes_one_set)
    except ValueError as error:
        print(repr(error))
        gui.log_error(str(error))
        gui.log("Start aborted")
        gui.enable_button(0)
        return
    stop_accuracy = gui.get_entry_value(5)
    population_size = gui.get_entry_value(2)
    population_noise = gui.get_entry_value(4)
    population_discard = gui.get_entry_value(3)
    reverse_fitness = gui.get_checkbox_value(6, 0)
    pyboard_port = gui.get_entry_value(0)
    random_low = gui.get_entry_value(8)
    random_high = gui.get_entry_value(9)
    number_of_values = gui.get_entry_value(10)

    recreate_usb = True
    gui.disable_entry(1)
    global paused
    if not paused:
        global parameter_per_cycle
        selected = gui.get_entry_value(1)
        if "size" in selected:
            parameter_per_cycle.append(population_size)
        elif "discard" in selected:
            parameter_per_cycle.append(population_discard)
        elif "noise" in selected:
            parameter_per_cycle.append(population_noise)
        elif "accuracy" in selected:
            parameter_per_cycle.append(stop_accuracy)
        elif "values" in selected:
            parameter_per_cycle.append(number_of_values)
    else:
        recreate_usb = False

    crossover_options = []

    for x, boolean in enumerate(gui.get_checkbox_values(7)):
        if boolean.get() is True:
            crossover_options.append(x + 1)
        x += 1

    config = create_config(number_of_values, stop_accuracy, population_size, population_discard, population_noise,
                           reverse_fitness, random_low, random_high, crossover_options)
    try:
        pyboard_port = controller.start_algorithm(config, pyboard_port, recreate_usb=recreate_usb)
        gui.log("PyBoard port is set to " + pyboard_port)
        global reply_thread
        reply_thread = threading.Thread(target=board_reply, args=(controller, gui))
        reply_thread.do_run = True
        reply_thread.start()
        gui.enable_buttons([1, 2, 3])
    except serial.serialutil.SerialException:
        gui.log_error("Failed connection to board")
        gui.log("Start aborted")
        gui.enable_button(0)
    finally:
        gui.enable_entry(0)


def pause_button_action(controller, gui):
    """
    Function handling algorithm pausing

    Disable gui buttons for working time, send communicate to board.

    @param controller: used to communicate with board
    @param gui: used to display results
    """
    gui.disable_buttons([0, 1, 2, 3])
    gui.log("Pausing")
    global paused
    paused = True
    controller.pause_algorithm()
    gui.enable_buttons([0, 1, 2])


def save_results(gui):
    """
    Save results for further displaying (listboxes and graphs), display most recent results
    """
    try:
        result = last_result
        gui.log_info("Result: ")
        for key, value in result.items():
            gui.log_info(str(key) + ": " + str(value))
        global full_times
        global run_number
        global full_memory_usage
        parmeter = parameter_per_cycle[run_number - 1]
        time = str(result['total_time'])
        memory = str(result['alloc_memory'])
        full_times.append(time)

        full_memory_usage.append(memory)

        gui.insert_listbox_data(0, run_number,
                                str(run_number) + "[" + parmeter + "]" + " - " +
                                time + "s")
        gui.insert_listbox_data(1, run_number,
                                str(run_number) + "[" + parmeter + "]" + " - " +
                                memory + "B")
    except AttributeError or ValueError:
        gui.log_error("Could not read results")
    run_number += 1


def stop_button_action(controller, gui, send_stop=True):
    """
    Function handling algorithm stopping

    Disable gui buttons for working time, send command to board. Additional save results for further displaying (listboxes
    and graphs)

    @param controller: used to communicate with board
    @param gui: used to display results
    @param send_stop: if false not sending command to board (only when board will stop by itself)
    """
    global reply_thread
    reply_thread.do_run = False
    reply_thread = None
    gui.disable_buttons([0, 1, 2, 3])
    gui.log("Stopping")
    save_results(gui)
    if send_stop:
        controller.stop_algorithm()
    global paused
    paused = False
    gui.enable_entry(0)
    gui.enable_button(0)


def restart_button_action(controller, gui, checkboxes_one_set):
    stop_button_action(controller, gui)
    start_button_action(controller, gui, checkboxes_one_set)


def draw_graph_button_action():
    """
    Draw time from run number graph with two lines: time and memory
    """

    graph = Graph("Graph", "run number", "value", parameter_per_cycle)
    graph.add_y_axis_data("time", full_times, 'lines+markers')
    graph.add_y_axis_data("memory usage", full_memory_usage, 'lines+markers')
    graph.show()


def debug_button_action(controller, gui):
    gui.log(controller.usb.read_debug())


def info_button_action():
    info = GUI("Parameters info", labels_column_anchor="w")
    boldfont = "default 12 bold"
    info.add_label("PyBoard port:", font=boldfont)
    info.add_label("Location of port used to communicate with PyBoard ex. /dev/ttyACM1")
    info.add_label("Graph parameter:", font=boldfont)
    info.add_label("The Y axis parameter for drawing data")
    info.add_label("Population size:", font=boldfont)
    info.add_label("Size of population (Value in range <1:x>)")
    info.add_label("Population discard:", font=boldfont)
    info.add_label("Percentage of discarded members with each generation (Value in range <0:1>)")
    info.add_label("Population noise:", font=boldfont)
    info.add_label("Chance of random mutation for each member (Value in range <0:1>)")
    info.add_label("Stop condition accuracy:", font=boldfont)
    info.add_label("Algorithm accuracy that affects the start of the stop condition")
    info.add_label("Population reverse fitness:", font=boldfont)
    info.add_label("Tells algorithm which is better: Lower fitness or higher")
    info.add_label("Member crossover options:", font=boldfont)
    info.add_label("List of allowed crossover types. Possible values: 1. One point 2. Multi point")
    info.add_label("Member min random:", font=boldfont)
    info.add_label("Initial values lower limit")
    info.add_label("Member max random:", font=boldfont)
    info.add_label("Initial values higher limit")
    info.add_label("Number of operator values:", font=boldfont)
    info.add_label("Number of fitness function variables")


if __name__ == '__main__':
    """
    Populating and starting gui
    """
    gui = GUI("Desktop STM GA Control Panel", 15)

    gui.add_text_entry("PyBoard port:")
    gui.add_combo_box("Graph parameter:", ["size", "discard", "noise", "stop accuracy", "no. of operator values"])
    gui.add_spinbox("Population size:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Population discard:", 0, 1, '%0.3f', 0.001)
    gui.add_spinbox("Population noise:", 0, 1, '%0.3f', 0.001)
    gui.add_spinbox("Stop condition accuracy:", 0, 1, '%1.9f', 0.000000001)

    gui.add_checkboxes("Population reverse fitness:", [""], False)
    gui.add_checkboxes("Member crossover options:", ["One point", "Multi point"], False)
    # rows with checkboxes that must have at least one option set
    checkboxes_one_set = [7]

    gui.add_spinbox("Member min random:", -9999, 9999, '%1.f', 1)
    gui.add_spinbox("Member max random:", -9999, 9999, '%1.f', 1)
    gui.add_spinbox("Number of operator values:", 1, 100, '%1.f', 1)

    gui.add_console()
    gui.log("Fitness caclulating function is located in fintess.py")
    gui.log("Please edit this function before running GUI")

    controller = Controller()

    gui.add_button("START", lambda: start_button_action(controller, gui, checkboxes_one_set))
    gui.add_button("STOP", lambda: stop_button_action(controller, gui))
    gui.add_button("RESTART", lambda: restart_button_action(controller, gui, checkboxes_one_set))
    gui.add_button("PAUSE", lambda: pause_button_action(controller, gui))
    gui.add_button("DRAW GRAPH", lambda: draw_graph_button_action())
    gui.add_button("DEBUG", lambda: debug_button_action(controller, gui))
    gui.add_button("INFO", lambda: info_button_action())
    gui.disable_buttons([1, 2, 3])

    gui.add_listbox()
    gui.insert_listbox_data(0, 0, "Time:")
    gui.add_listbox()
    gui.insert_listbox_data(1, 0, "Memory:")
    gui.work()
