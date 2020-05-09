from tkinter import *
from tkinter import scrolledtext


def stop_algorithm(gui):
    gui.log("Stopping")
    # TODO pass STOP command to board using VCP


def restart_algorithm(gui):
    gui.log("Restarting")
    stop_algorithm(gui)
    start_algorithm(gui)


def start_algorithm(gui):
    gui.log("Starting")
    try:
        gui.check_values()
    except ValueError as error:
        print(repr(error))
        gui.log_error(str(error))
        gui.log("Start aborted")
        return
    population_chance_bonus = gui.population_chance_bonus_spinbox.get()
    population_size = gui.population_size_spinbox.get()
    population_noise = gui.population_noise_spinbox.get()
    population_discard = gui.population_discard_spinbox.get()

    mutation_options = []
    x = 1
    for boolean in gui.mutation_states:
        if boolean.get() is True:
            mutation_options.append(x)
        x += 1

    crossover_options = []
    x = 1
    for boolean in gui.crossover_states:
        if boolean.get() is True:
            crossover_options.append(x)
        x += 1
    config = {
        "population_size" : population_size,
        "population_discard" : population_discard,
        "population_chance_bonus" : population_chance_bonus,
        "population_noise" : population_noise,
        "member_mutation_options" : mutation_options,
        "member_crossover_options" : crossover_options
    }
    # TODO pass config to board using VCP


class GUI:
    def __init__(self):
        self.window = Tk()

        self.window.title("Desktop STM GA Control Panel")
        self.window.resizable(width=False, height=False)

        entries_column = 1
        entries_column_anchor = "w"
        labels_column = 0
        labels_column_anchor = "e"

        spinbox_width = 5
        buttons_width = 10

        population_size_default_value = 100

        self.population_size_min = 0
        self.population_size_max = 9999
        self.population_percentage_values_min = 0
        self.population_percentage_values_max = 1
        self.population_chance_bonus_min = 1
        self.population_chance_bonus_max = 9999

        self.mutation_texts = ["Random resetting", "Swap", "Scramble", "Inversion"]
        self.mutation_states = [BooleanVar(), BooleanVar(), BooleanVar(), BooleanVar()]
        self.mutation_states[0].set(True)

        self.crossover_texts = ["One point", "Multi point"]
        self.crossover_states = [BooleanVar(), BooleanVar()]
        self.crossover_states[0].set(True)

        labels = []
        row = 1
        self.label_names = ["Population size:", "Population discard:", "Population noise:",
                            "Population chance bonus:",
                            "Member mutation options:", "Member crossover options:"]
        for label_name in self.label_names:
            new_label = Label(self.window, text=label_name)
            new_label.grid(column=labels_column, row=row, sticky=labels_column_anchor)
            labels.append(new_label)
            row += 1

        # entries
        default_size = IntVar()
        default_size.set(population_size_default_value)
        self.population_size_spinbox = Spinbox(self.window, from_=self.population_size_min, to=self.population_size_max,
                                               width=spinbox_width,
                                               textvariable=default_size)
        self.population_size_spinbox.grid(column=entries_column, row=1, sticky=entries_column_anchor)
        self.population_size_spinbox.focus()

        self.population_discard_spinbox = Spinbox(self.window, from_=self.population_percentage_values_min,
                                                  to=self.population_percentage_values_max,
                                                  width=spinbox_width, format='%0.3f', increment=0.001)
        self.population_discard_spinbox.grid(column=entries_column, row=2, sticky=entries_column_anchor)

        self.population_noise_spinbox = Spinbox(self.window, from_=self.population_percentage_values_min,
                                                to=self.population_percentage_values_max,
                                                width=spinbox_width, format='%0.3f', increment=0.001)
        self.population_noise_spinbox.grid(column=entries_column, row=3, sticky=entries_column_anchor)

        self.population_chance_bonus_spinbox = Spinbox(self.window, from_=self.population_chance_bonus_min,
                                                       to=self.population_chance_bonus_max,
                                                       width=spinbox_width, format='%0.3f', increment=0.001)
        self.population_chance_bonus_spinbox.grid(column=entries_column, row=4, sticky=entries_column_anchor)

        self.member_mutation_option1 = Checkbutton(self.window, text=self.mutation_texts[0],
                                                   var=self.mutation_states[0])
        self.member_mutation_option1.grid(column=entries_column, row=5, sticky=entries_column_anchor)
        self.member_mutation_option2 = Checkbutton(self.window, text=self.mutation_texts[1],
                                                   var=self.mutation_states[1])
        self.member_mutation_option2.grid(column=entries_column + 1, row=5, sticky=entries_column_anchor)
        self.member_mutation_option3 = Checkbutton(self.window, text=self.mutation_texts[2],
                                                   var=self.mutation_states[2])
        self.member_mutation_option3.grid(column=entries_column + 2, row=5, sticky=entries_column_anchor)
        self.member_mutation_option4 = Checkbutton(self.window, text=self.mutation_texts[3],
                                                   var=self.mutation_states[3])
        self.member_mutation_option4.grid(column=entries_column + 3, row=5, sticky=entries_column_anchor)

        self.member_crossover_option1 = Checkbutton(self.window, text=self.crossover_texts[0],
                                                    var=self.crossover_states[0])
        self.member_crossover_option1.grid(column=entries_column, row=6, sticky=entries_column_anchor)
        self.member_crossover_option2 = Checkbutton(self.window, text=self.crossover_texts[1],
                                                    var=self.crossover_states[1])
        self.member_crossover_option2.grid(column=entries_column + 1, row=6, sticky=entries_column_anchor)

        # buttons
        self.stop_btn = Button(self.window, text="STOP", command=lambda: stop_algorithm(self), width=buttons_width)
        self.stop_btn.grid(column=4, row=2)

        self.restart_btn = Button(self.window, text="RESTART", command=lambda: restart_algorithm(self),
                                  width=buttons_width)
        self.restart_btn.grid(column=4, row=3)

        self.start_btn = Button(self.window, text="START", command=lambda: start_algorithm(self), width=buttons_width)
        self.start_btn.grid(column=4, row=1)

        self.console = scrolledtext.ScrolledText(self.window)
        self.console.grid(column=0, row=11, columnspan=5, padx=5, pady=5)

    def log(self, text):
        self.console.insert('end', text + '\n')

    def log_info(self, text):
        self.console.insert('end', "\tINFO:" + text + '\n')

    def log_error(self, text):
        self.console.insert('end', "\tERROR:" + text + '\n')

    def work(self):
        self.window.mainloop()

    def check_values(self):
        spinbox_value = int(self.population_size_spinbox.get())
        if spinbox_value > self.population_size_max:
            raise ValueError('Population size exceeded MAX: ' + str(self.population_size_max))
        if spinbox_value < self.population_size_min:
            raise ValueError('Population size under MIN: ' + str(self.population_size_min))

        spinbox_value = float(self.population_chance_bonus_spinbox.get())
        if spinbox_value > self.population_chance_bonus_max:
            raise ValueError('Population chance bonus exceeded MAX: ' + str(self.population_chance_bonus_max))
        if spinbox_value < self.population_chance_bonus_min:
            raise ValueError('Population chance bonus under MIN: ' + str(self.population_percentage_values_min))

        spinbox_value = float(self.population_discard_spinbox.get())
        if spinbox_value > self.population_percentage_values_max:
            raise ValueError('Population discard exceeded MAX: ' + str(self.population_percentage_values_max))
        if spinbox_value < self.population_percentage_values_min:
            raise ValueError('Population discard under MIN: ' + str(self.population_percentage_values_min))

        spinbox_value = float(self.population_noise_spinbox.get())
        if spinbox_value > self.population_percentage_values_max:
            raise ValueError('Population noise exceeded MAX: ' + str(self.population_percentage_values_max))
        if spinbox_value < self.population_percentage_values_min:
            raise ValueError('Population noise under MIN: ' + str(self.population_chance_bonus_min))

        found_true = False
        for boolean in self.mutation_states:
            if boolean.get() is True:
                found_true = True
        if found_true is False:
            raise ValueError('At least one mutation option must be selected')

        found_true = False
        for boolean in self.crossover_states:
            if boolean.get() is True:
                found_true = True
        if found_true is False:
            raise ValueError('At least one crossover option must be selected')


if __name__ == '__main__':
    gui = GUI()
    gui.work()
