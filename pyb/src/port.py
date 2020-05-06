"""
File contains code necessary to run algorithm through USB VCP.
@author: Jakub Chodubski
"""
import pyb
import ujson

from pyb.src.inform import Inform


class Port:
    """
    Class used to communicate via USB
    """

    def __init__(self):
        self.usb = pyb.USB_VCP()
        self.list: list = []
        Inform.waiting()
        while not self.usb.isconnected():
            pyb.delay(100)

    def attach(self, index, value):
        self.list.insert(index, value)

    def send(self):
        dic = {
            "type": "1",  # type of communication; more on that in __init__
            "val": self.list
        }
        to_send = ujson.dump(dic)
        print("Sent: ", self.usb.write(to_send), "bytes")

    def read(self):
        received: bytes = self.usb.readline()
        str_rcv = received.decode('utf-8')
        dictionary = ujson.loads(received)
        if dictionary["type"] == 9:
            Inform.error()
        return dictionary