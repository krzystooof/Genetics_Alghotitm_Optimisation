""" Class that implements polynomial input for member

polynomial = sum from i to n of a(i) * x to the power of i ex 5x^5 - 4x2 + 1
values - list of polynomial values reversed,
    ex polynomial = ax^2+b values=[b,0,a], (ax^2+0x+b)
"""


class Operator:
    def __init__(self, values):
        self.values = values
