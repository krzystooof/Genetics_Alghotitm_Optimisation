"""This module contains code used to communicate with pyboard"""
import serial
import json
from time import sleep


class USB:
    """
    Handles communication via USB VCP
    @author: Jakub Chodubski
    """

    def __init__(self, comm_port=None):
        """Initiates connection. Waits till connected."""
        if comm_port is None:
            # Defaults to one of 2 ports
            try:
                self.usb = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
            except serial.serialutil.SerialException:
                self.usb = serial.Serial('/dev/ttyACM1', 9600, timeout=0)
        else:
            self.usb = serial.Serial(comm_port, 9600, timeout=0)

        self.fifo = []
        self.dictionary = dict()
        while not self.usb.is_open:
            self.usb.open()
            sleep(0.1)

    def attach(self, key, value):
        self.dictionary[key] = value

    def send(self):
        string = json.dumps(self.dictionary)
        bytes_to_send = string.encode('utf-8')
        self.usb.write(bytes_to_send)
        self.dictionary = dict()

    def read(self):
        """Always returns python dictionary. Read 'type' to see what's inside"""
        if self.usb.in_waiting != 0:
            read = self.usb.readline()
            read_string = read.decode('utf-8')

            # Catching pyboard tracebacks
            if read_string[0] != '{':
                read_traceback = self.usb.readlines()
                for line in read_traceback:
                    read_string += line.decode('utf-8')
                sleep(0.3)
                if self.usb.in_waiting != 0:
                    for line in read_traceback:
                        read_string += line.decode('utf-8')
                raise ConnectionAbortedError(read_string)

            # Keep reading from buffer until jsons are complete
            while read_string.count('{') != read_string.count('}'):
                read = self.usb.readline()
                read_string += read.decode('utf-8')

            # Split and return
            self.push(read_string)
        return self.pop()

    def read_debug(self):
        """Reads and clears input buffer"""
        if self.usb.in_waiting != 0:
            sleep(1)
            read = self.usb.readlines()
            read_string = ""
            for line in read:
                read_string += line.decode('utf-8')
            return read_string
        else:
            return ""

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
            print("INCOMING MESSAGE: " + message)
            return json.loads(message)
        return {'type': 0}
