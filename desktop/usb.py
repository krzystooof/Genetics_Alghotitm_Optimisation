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

    def read(self):
        """Always returns python dictionary. Read 'type' to see what's inside"""
        if self.usb.in_waiting != 0:
            read = self.usb.readline()
            read_string = read.decode('utf-8')
            # Catching pyboard tracebacks
            if read_string[0] != '{':
                sleep(1)
                read_traceback = self.usb.readlines()
                for line in read_traceback:
                    read_string += line.decode('utf-8')
                raise ConnectionAbortedError(read_string)
            while read_string.count('{') != read_string.count('}'):
                read = self.usb.readline()
                read_string += read.decode('utf-8')
            try:
                return json.loads(read_string)
            except json.decoder.JSONDecodeError:
                raise ValueError(read_string)
        else:
            return {'type': 0}

    def read_debug(self):
        if self.usb.in_waiting != 0:
            sleep(1)
            read = self.usb.readlines()
            read_string = ""
            for line in read:
                read_string += line.decode('utf-8')
            return read_string
        else:
            return ""
