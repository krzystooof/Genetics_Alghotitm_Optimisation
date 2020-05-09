from tkinter import *
from tkinter import scrolledtext


def stop_alghoritm():
    pass


def restart_alghoritm():
    pass


def start_alghoritm():
    pass


class GUI:
    window = Tk()
    window.title("Desktop STM GA Control Panel")

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

    mutation1_text = "Random resetting"
    mutation1_state = BooleanVar()
    mutation1_state.set(True)
    mutation2_text = "Swap"
    mutation2_state = BooleanVar()
    mutation2_state.set(True)
    mutation3_text = "Scramble"
    mutation3_state = BooleanVar()
    mutation3_state.set(True)
    mutation4_text = "Inversion"
    mutation4_state = BooleanVar()
    mutation4_state.set(True)

    crossover1_text = "One point"
    crossover1_state = BooleanVar()
    crossover1_state.set(True)
    crossover2_text = "Multi point"
    crossover2_state = BooleanVar()
    crossover2_state.set(True)

    labels = []
    row = 1
    label_names = ["Population size:", "Population discard:", "Population chance bonus:", "Population chance bonus:",
                   "Member mutation options:", "Member crossover options:"]
    for label_name in label_names:
        new_label = Label(window, text=label_name)
        new_label.grid(column=labels_column, row=row, sticky=labels_column_anchor)
        labels.append(new_label)
        row += 1

    default_size = IntVar()
    default_size.set(population_size_default_value)
    population_size_spinbox = Spinbox(window, from_=population_size_min, to=population_size_max, width=spinbox_width,
                                      textvariable=default_size)
    population_size_spinbox.grid(column=entries_column, row=1, sticky=entries_column_anchor)

    population_discard_spinbox = Spinbox(window, from_=population_percentage_values_min,
                                         to=population_percentage_values_max,
                                         width=spinbox_width, format='%0.3f', increment=0.001)
    population_discard_spinbox.grid(column=entries_column, row=2, sticky=entries_column_anchor)

    population_noise_spinbox = Spinbox(window, from_=population_percentage_values_min,
                                       to=population_percentage_values_max,
                                       width=spinbox_width, format='%0.3f', increment=0.001)
    population_noise_spinbox.grid(column=entries_column, row=3, sticky=entries_column_anchor)

    population_chance_bonus_spinbox = Spinbox(window, from_=population_percentage_values_min,
                                              to=population_percentage_values_max,
                                              width=spinbox_width, format='%0.3f', increment=0.001)
    population_chance_bonus_spinbox.grid(column=entries_column, row=4, sticky=entries_column_anchor)

    member_mutation_option1 = Checkbutton(window, text=mutation1_text, var=mutation1_state)
    member_mutation_option1.grid(column=entries_column, row=5, sticky=entries_column_anchor)
    member_mutation_option2 = Checkbutton(window, text=mutation2_text, var=mutation2_state)
    member_mutation_option2.grid(column=entries_column + 1, row=5, sticky=entries_column_anchor)
    member_mutation_option3 = Checkbutton(window, text=mutation3_text, var=mutation3_state)
    member_mutation_option3.grid(column=entries_column + 2, row=5, sticky=entries_column_anchor)
    member_mutation_option4 = Checkbutton(window, text=mutation4_text, var=mutation4_state)
    member_mutation_option4.grid(column=entries_column + 3, row=5, sticky=entries_column_anchor)

    member_crossover_option1 = Checkbutton(window, text=crossover1_text, var=crossover1_state)
    member_crossover_option1.grid(column=entries_column, row=6, sticky=entries_column_anchor)
    member_crossover_option2 = Checkbutton(window, text=crossover2_text, var=crossover2_state)
    member_crossover_option2.grid(column=entries_column + 1, row=6, sticky=entries_column_anchor)

    stop_btn = Button(window, text="STOP", command=stop_alghoritm, width=buttons_width)
    stop_btn.grid(column=4, row=2)

    restart_btn = Button(window, text="RESTART", command=restart_alghoritm, width=buttons_width)
    restart_btn.grid(column=4, row=3)

    start_btn = Button(window, text="START", command=start_alghoritm, width=buttons_width)
    start_btn.grid(column=4, row=1)

    # message_box = scrolledtext.ScrolledText(window, height=10)
    #
    # message_box.grid(column=0, row=11, columnspan=5, padx=5, pady=5)

    window.mainloop()


if __name__ == '__main__':
    gui = GUI()
