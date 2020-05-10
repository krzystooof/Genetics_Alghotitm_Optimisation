"""This module contains code used to communicate with pyboard"""
import serial
from time import sleep

class USB:
    """
    Handles communication via USB VCP
    @author: Jakub Chodubski
    """
    def __init__(self, comm_port='/dev/ttyACM1'):  # ttyACM1 is default pyboard port in Linux
        """Initiates connection. Waits till connected."""
        self.usb = serial.Serial(port=comm_port)
        self.usb.open()
        self.list: list = []
        while not self.usb.is_open():
            self.usb.open()
            sleep(0.1)

    def attach(self):
        pass

    def send(self):
        pass

    def read(self):
        pass
