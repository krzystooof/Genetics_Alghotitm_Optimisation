"""File contains code necessary to run algorithm on pyboard."""
import pyb
import ujson


class VCP:  # TODO make this static
    """
    Class used to communicate via USB VCP. Needs initialization.
    @author: Jakub Chodubski
    """

    def __init__(self):
        """Opens VCP and waits for connection"""
        self.usb = pyb.USB_VCP()
        self.dictionary = dict()
        self.fifo = []
        Inform.waiting()
        while not self.usb.isconnected():
            pyb.delay(100)

    def attach(self, key, element):
        """Drop data to the package before sending it"""
        self.dictionary[key] = element

    def send(self):
        string = ujson.dumps(self.dictionary)
        bytes_to_send = string.encode('utf-8')
        self.usb.write(bytes_to_send)
        self.dictionary = dict()

    def read(self):
        """
        Reads data from USB VCP. Always returns python dictionary with at least
        'type' field. Type values:
        0 means there was no new data on usb buffer
        1 means desktop client encountered a problem
        2 means config was transferred
        3 means data was successfully transferred
        4 means there is data regarding algorithm control
        ...
        9 means there is data to feed to algorithm

        Type 3 is internal type and will not be forwarded.
        """
        if self.usb.any():
            read = self.usb.readline()
            read_string = read.decode('utf-8')

            # Keep reading from buffer until json is complete
            while read_string.count('{') != read_string.count('}'):
                read = self.usb.readline()
                read_string += read.decode('utf-8')

            # Split and return
            self.push(read_string)
        return self.pop()

    def push(self, line):
        """Splits jsons string into single messages and puts in fifo"""
        if line[0] != '{':
            raise ValueError("Could not parse json: " + line)
        message = ""
        for character in line:
            message += character
            if message.count('{') == message.count('}'):
                self.fifo.insert(0, message)
                message = ""

    def pop(self):
        """Reads messages from fifo"""
        if len(self.fifo) != 0:
            message = self.fifo.pop()
            return ujson.loads(message)
        return {'type': 0}


class Inform:
    """
    This class is used to signalize pyboard status via LEDs. It is fully static to optimize runtime.
    Should be used every time pyboard changes its state or important event happens.
    @author: Jakub Chodubski
    """
    state = 0

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
