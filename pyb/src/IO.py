stm_pins = [0 for x in range(32)]


class IO:

    def write_pin(self, pin, value):
        stm_pins[pin] = value

    def read_pin(self, pin):
        print("Value of Pin", pin, "is ")
        print(stm_pins[pin])

    def on_off_toggle(self, pin):
        print("Toggle switched value of Pin", pin)
        if stm_pins[pin] == 1:
            stm_pins[pin] = 0
        else:
            stm_pins[pin] = 1
