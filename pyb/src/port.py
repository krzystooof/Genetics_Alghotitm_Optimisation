"""File contains code necessary to run algorithm on pyboard."""
import pyb
import ujson


class VCP:
    """
    Class used to communicate via USB VCP. Needs initialization.
    @author: Jakub Chodubski
    """

    def __init__(self):
        """Opens VCP and waits for connection"""
        self.usb = pyb.USB_VCP()
        self.list: list = []
        Inform.waiting()
        while not self.usb.isconnected():
            pyb.delay(100)

    def attach(self, index, value):
        """Drop data to the package before sending it"""
        self.list.insert(index, value)

    def send(self):
        """Sends attached data. Clears buffer of attach()."""
        dic = {
            "type": "1",  # type of communication; more on that in __init__
            "val": self.list
        }
        to_send = ujson.dump(dic)
        print("Sent: ", self.usb.write(to_send), "bytes")

    def read(self):
        """
        Reads data from USB VCP. Always returns python dictionary with at least
        'type' field. Type values:
        0 means there was no new data on usb buffer
        1 means there is data to feed to algorithm
        2 means there is data regarding algorithm control
        3 means data was successfully transferred
        ...
        9 means desktop client encountered a problem

        Type 3 is internal type and will not be forwarded.
        """
        received: bytes = self.usb.readline()
        str_rcv = received.decode('utf-8')
        dictionary = ujson.loads(str_rcv)
        if dictionary["type"] == 9:
            Inform.error()
        return dictionary


class IO:
    """
    Gives access to individual pins.
    """
    stm_pins = [0 for x in range(32)]

    @staticmethod
    def write_pin(pin, value):
        """method desc..."""
        IO.stm_pins[pin] = value

    @staticmethod
    def read_pin(pin):
        """
        method desc...
        @param pin:  param desc...
        """
        print("Value of Pin", pin, "is ")
        print(IO.stm_pins[pin])

    @staticmethod
    def on_off_toggle(pin):
        print("Toggle switched value of Pin", pin)
        if IO.stm_pins[pin] == 1:
            IO.stm_pins[pin] = 0
        else:
            IO.stm_pins[pin] = 1


class Inform:
    """
    This class is used to signalize pyboard status via LEDs. It is fully static to optimize runtime.
    Should be used every time pyboard changes its state or important event happens.
    @author: Jakub Chodubski
    """
    state: int = 0

    @staticmethod
    def waiting():  # green on
        """
        Should be used if the board is waiting for new inputs.
        """
        Inform.state = 0
        pyb.LED(1).on()
        pyb.LED(2).off()
        pyb.LED(3).off()

    @staticmethod
    def running():  # blue on
        """
        Use this if board is not accepting any inputs at the moment.
        Any data send via USB VCP to board will be queued.
        """
        Inform.state = 1
        pyb.LED(1).off()
        pyb.LED(2).on()
        pyb.LED(3).off()

    @staticmethod
    def error():  # red on
        """
        Algorithm encountered a problem.
        Board is waiting for debug and reset.
        """
        Inform.state = 2
        pyb.LED(1).off()
        pyb.LED(2).off()
        pyb.LED(3).on()

    @staticmethod
    def connected():  # quick flash green, blued
        """
        Signal Virtual Comm Port has been connected.
        After signaling is done previous state will be displayed.
        """
        pyb.LED(1).off()
        pyb.LED(2).on()
        pyb.LED(3).on()
        Inform.correct_led()

    @staticmethod
    def correct_led():
        """Method used to correct currently displayed LEDs to state saved in Inform.state"""
        if Inform.state == 0:
            Inform.waiting()

        if Inform.state == 1:
            Inform.running()

        if Inform.state == 2:
            Inform.error()
