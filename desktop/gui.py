"""This module contains code used to graphically present control panel"""

from tkinter import *
from tkinter import scrolledtext


class GUI:
    """
        Graphical user interface using tkinter
        @author: Krzysztof Greczka
    """

    def __init__(self, window_title):
        self.window = Tk()

        self.window.title(window_title)
        self.window.resizable(width=False, height=False)

        # default values - able to change after init
        self.entries_width = 5
        self.buttons_width = 10
        self.entries_column = 1
        self.entries_column_anchor = "w"
        self.labels_column = 0
        self.labels_column_anchor = "e"
        self.buttons_column = 2

        # algorithm specific values = do not change
        self.free_row = 0
        self.free_button_row = 0
        self.labels = []
        self.entries = []
        self.min_max_spinbox_values = {}
        self.checkbox_values = {}
        self.buttons = []

    def add_text_entry(self, text):
        new_label = Label(self.window, text=text)
        new_label.grid(column=self.labels_column, row=self.free_row, sticky=self.labels_column_anchor)
        self.labels.append(new_label)

        new_entry = Entry(self.window, width=self.entries_width)
        new_entry.grid(column=self.entries_column, row=self.free_row, sticky=self.entries_column_anchor)
        self.entries.append(new_entry)

        self.free_row += 1

    def add_spinbox(self, text, min_value, max_value, format, increment):
        new_label = Label(self.window, text=text)
        new_label.grid(column=self.labels_column, row=self.free_row, sticky=self.labels_column_anchor)
        self.labels.append(new_label)

        new_spinbox = Spinbox(self.window, from_=min_value,
                              to=max_value,
                              width=self.entries_width, format=format, increment=increment)
        new_spinbox.grid(column=self.entries_column, row=self.free_row, sticky=self.entries_column_anchor)
        self.entries.append(new_spinbox)

        values = [min_value, max_value]
        self.min_max_spinbox_values[self.free_row] = values

        self.free_row += 1

    def add_checkboxes(self, text, options_texts, def_value):
        new_label = Label(self.window, text=text)
        new_label.grid(column=self.labels_column, row=self.free_row, sticky=self.labels_column_anchor)
        self.labels.append(new_label)

        checkbuttons = []
        states = []
        column = self.entries_column
        for text in options_texts:
            state = BooleanVar()
            state.set(def_value)
            new_checkbutton = Checkbutton(self.window, text=text, var=state)
            new_checkbutton.grid(column=column, row=self.free_row, sticky=self.entries_column_anchor)
            states.append(state)
            checkbuttons.append(new_checkbutton)
            column += 1
            if column >= self.buttons_column:
                self.buttons_column = column + 1
        self.checkbox_values[self.free_row] = states
        self.entries.append(checkbuttons)
        self.free_row += 1

    def add_button(self, text, function):
        new_button = Button(self.window, text=text, command=function, width=self.buttons_width)
        new_button.grid(column=self.buttons_column, row=self.free_button_row)
        self.buttons.append(new_button)
        self.free_button_row += 1

    def add_console(self):
        self.console = scrolledtext.ScrolledText(self.window)
        self.console.grid(column=0, row=self.free_row, columnspan=self.buttons_column, padx=5, pady=5)

    def get_label_text(self, row):
        return self.labels[row].cget("text")

    def get_entry_value(self, row):
        try:
            return self.entries[row].get()
        except AttributeError or IndexError:
            raise IndexError("No entry in this row")

    def get_checkbox_value(self, row, number):
        try:
            return self.checkbox_values[row][number].get()
        except KeyError:
            raise IndexError("No checkbox in this row")
        except IndexError:
            raise IndexError("No checkbox with this number")

    def log(self, text):
        try:
            self.console.insert('end', text + '\n')
        finally:
            print(text + '\n')

    def log_info(self, text):
        try:
            self.console.insert('end', "\tINFO:" + text + '\n')
        finally:
            print("\tINFO:" + text + '\n')

    def log_error(self, text):
        try:
            self.console.insert('end', "\tERROR:" + text + '\n')
        finally:
            print("\tERROR:" + text + '\n')

    def work(self):
        self.window.mainloop()

    def check_values(self, one_checked):
        # one_checked - list of checkboxes rows that at least one option must be selected
        for key, value in self.min_max_spinbox_values.items():
            spinbox_value = float(self.get_spinbox_value(key))
            if spinbox_value > value[1]:
                raise ValueError(self.get_label_text(key) + ' exceeded MAX: ' + str(value[1]))
            if spinbox_value < value[0]:
                raise ValueError(self.get_label_text(key) + ' number under MIN: ' + str(value[1]))
        for key, value in self.checkbox_values.items():
            if key in one_checked:
                found_true = False
                for bool in value:
                    if bool.get() is True:
                        found_true = True
                if found_true is False:
                    raise ValueError('At least one ' + self.get_label_text(key) + ' must be selected')
