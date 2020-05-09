from tkinter import *
from tkinter import scrolledtext


def stop_alghoritm(gui):
    gui.log("Stop Called")



def restart_alghoritm(gui):
    gui.log("Retart Called")


def start_alghoritm(gui):
    pass

class GUI:
    def __init__(self):
        self.window = Tk()
        self.crossover2_state = BooleanVar()
        self.crossover1_state = BooleanVar()
        self.mutation4_state = BooleanVar()
        self.mutation3_state = BooleanVar()
        self.mutation2_state = BooleanVar()
        self.mutation1_state = BooleanVar()

        self.window.title("Desktop STM GA Control Panel")
        self.window.resizable(width=False, height=False)

        entries_column = 1
        entries_column_anchor = "w"
        labels_column = 0
        labels_column_anchor = "e"

        spinbox_width = 5
        buttons_width = 10

        population_size_default_value = 100
        population_size_min = 0
        population_size_max = 9999

        population_percentage_values_min = 0
        population_percentage_values_max = 1

        population_chance_bonus_min = 1
        population_chance_bonus_max = 9999

        self.mutation1_text = "Random resetting"
        self.mutation1_state.set(True)
        self.mutation2_text = "Swap"
        self.mutation2_state.set(True)
        self.mutation3_text = "Scramble"
        self.mutation3_state.set(True)
        self.mutation4_text = "Inversion"
        self.mutation4_state.set(True)

        self.crossover1_text = "One point"
        self.crossover1_state.set(True)
        self.crossover2_text = "Multi point"
        self.crossover2_state.set(True)

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
        self.population_size_spinbox = Spinbox(self.window, from_=population_size_min, to=population_size_max,
                                               width=spinbox_width,
                                               textvariable=default_size)
        self.population_size_spinbox.grid(column=entries_column, row=1, sticky=entries_column_anchor)
        self.population_size_spinbox.focus()

        self.population_discard_spinbox = Spinbox(self.window, from_=population_percentage_values_min,
                                                  to=population_percentage_values_max,
                                                  width=spinbox_width, format='%0.3f', increment=0.001)
        self.population_discard_spinbox.grid(column=entries_column, row=2, sticky=entries_column_anchor)

        self.population_noise_spinbox = Spinbox(self.window, from_=population_percentage_values_min,
                                                to=population_percentage_values_max,
                                                width=spinbox_width, format='%0.3f', increment=0.001)
        self.population_noise_spinbox.grid(column=entries_column, row=3, sticky=entries_column_anchor)

        self.population_chance_bonus_spinbox = Spinbox(self.window, from_=population_chance_bonus_min,
                                                       to=population_chance_bonus_max,
                                                       width=spinbox_width, format='%0.3f', increment=0.001)
        self.population_chance_bonus_spinbox.grid(column=entries_column, row=4, sticky=entries_column_anchor)

        self.member_mutation_option1 = Checkbutton(self.window, text=self.mutation1_text, var=self.mutation1_state)
        self.member_mutation_option1.grid(column=entries_column, row=5, sticky=entries_column_anchor)
        self.member_mutation_option2 = Checkbutton(self.window, text=self.mutation2_text, var=self.mutation2_state)
        self.member_mutation_option2.grid(column=entries_column + 1, row=5, sticky=entries_column_anchor)
        self.member_mutation_option3 = Checkbutton(self.window, text=self.mutation3_text, var=self.mutation3_state)
        self.member_mutation_option3.grid(column=entries_column + 2, row=5, sticky=entries_column_anchor)
        self.member_mutation_option4 = Checkbutton(self.window, text=self.mutation4_text, var=self.mutation4_state)
        self.member_mutation_option4.grid(column=entries_column + 3, row=5, sticky=entries_column_anchor)

        self.member_crossover_option1 = Checkbutton(self.window, text=self.crossover1_text, var=self.crossover1_state)
        self.member_crossover_option1.grid(column=entries_column, row=6, sticky=entries_column_anchor)
        self.member_crossover_option2 = Checkbutton(self.window, text=self.crossover2_text, var=self.crossover2_state)
        self.member_crossover_option2.grid(column=entries_column + 1, row=6, sticky=entries_column_anchor)

        # buttons
        self.stop_btn = Button(self.window, text="STOP", command=lambda: stop_alghoritm(self), width=buttons_width)
        self.stop_btn.grid(column=4, row=2)

        self.restart_btn = Button(self.window, text="RESTART", command=lambda: restart_alghoritm(self),
                                  width=buttons_width)
        self.restart_btn.grid(column=4, row=3)

        self.start_btn = Button(self.window, text="START", command=lambda: start_alghoritm(self), width=buttons_width)
        self.start_btn.grid(column=4, row=1)

        self.console = scrolledtext.ScrolledText(self.window)
        self.console.grid(column=0, row=11, columnspan=5, padx=5, pady=5)

    def log(self, text):
        self.console.insert('end', text + '\n')

    def work(self):
        self.window.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.work()
