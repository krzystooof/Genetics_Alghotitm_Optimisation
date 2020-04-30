from machine import SPI


class Port:

    def __init__(self):
        spi = SPI(id=1, baundrate=100000, polarity=0, phase=0)
        SPI.init(baudrate=1000000, *, polarity=0, phase=0, bits=8, firstbit=SPI.MSB, sck=None, mosi=None, miso=None, pins=(SCK, MOSI, MISO))
        # line above will be corrected once access to dev board is given
        self.listen_mode = True

    def send(self, arg: list):
        self.listen_mode = False
        for x in range(0,len(arg)):
            buf = arg[x]
            SPI.write(buf)
        self.listen_mode = True
