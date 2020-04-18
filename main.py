import timeit
from unittest.mock import MagicMock

start = timeit.default_timer()

StmPins = [0 for x in range(32)]

class Configuration:

    def load(self):
        plik = open('C:\\Users\\Gregori\\PycharmProjects\\micropython-example\\Dane.txt.txt')
        print(plik.read())
        print("Wczytywanie danych z pliku")
        plik.close()

    def get_discard(self):
        return self.discard()

    def population_size(self):
        return self.population_size()


config = Configuration()
config.load()


class IO:

    def write_pin(self, pin, value):
        StmPins[pin] = value

    def read_pin(self, pin):
        print("Value of Pin", pin, "is ")
        print(StmPins[pin])

    def on_off_toggle(self, pin):
        print("Toggle switched value of Pin", pin)
        if StmPins[pin] == 1:
            StmPins[pin] = 0
        else:
            StmPins[pin] = 1


STM = IO()
STM.read_pin(1)
STM.write_pin(1, 1)
STM.read_pin(1)
STM.on_off_toggle(1)
STM.read_pin(1)


#Na to nie patrzcie
print("Mock")  
Pin = MagicMock()
Pin.x = 1
print(Pin.x)

stop = timeit.default_timer()

print('Time of program: ', stop - start, 's')
