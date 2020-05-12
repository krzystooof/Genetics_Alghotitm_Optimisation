from desktop.gui import GUI
from desktop.usb import USB
from desktop.alghoritm_control import *

if __name__ == '__main__':
    usb = USB()
    gui = GUI("Desktop STM GA Control Panel")

    gui.add_text_entry("PyBoard port:")
    gui.add_spinbox("Generations:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Population size:", 0, 9999, '%1.f', 1)
    gui.add_spinbox("Population discard:", 0, 1, '%0.3f', 0.001)
    gui.add_spinbox("Population noise:", 0, 1, '%0.3f', 0.001)
    gui.add_spinbox("Population chance bonus::", 1, 9999, '%1.3f', 0.001)

    gui.add_checkboxes("Population reverse fitness:", [""], False)
    gui.add_checkboxes("Member mutation options:", ["Random resetting", "Swap", "Scramble", "Inversion"], False)
    gui.add_checkboxes("Member crossover options:", ["One point", "Multi point"], False)

    gui.add_console()

    checkboxes_one_set = [7, 8]
    start_button_action = lambda: start_algorithm(gui, usb, checkboxes_one_set)
    gui.add_button("START", start_button_action)
    stop_button_action = lambda: stop_algorithm(gui, usb)
    gui.add_button("STOP", stop_button_action)
    restart_button_action = lambda: restart_algorithm(gui, usb)
    gui.add_button("RESTART", restart_button_action)
    stop_button_action = lambda: stop_algorithm(gui, usb)
    gui.add_button("START", stop_button_action)

    # must be at the end of main
    gui.work()
