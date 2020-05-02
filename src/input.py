class Operator:
    # polynomial = sum from i to n of a i * x to the power of i
    # ex 5x^5 - 4x2 + 1
    def __init__(self, values):
        # input - list of polynomial values reversed,
        # ex polynomial = ax^2+b values=[b,0,a], 0 - at index 1 there is 0x (ax^2+0x+b)

        self.values = values
