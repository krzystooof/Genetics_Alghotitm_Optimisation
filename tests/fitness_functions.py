def dynamic_object_sim(list_of_values):
    import numpy as np
    import math
    M = np.array([1.995908286, -0.996008084, 0.000024949, 0.000049899, 0.000024949])
    tsim = 30  # [s]
    ts = 0.01  # [s]
    t = np.arange(0, tsim, ts)  # [s]
    y = np.zeros(t.size)
    u = np.zeros(t.size)
    r = np.ones(t.size)
    Kp = list_of_values[0]
    Ki = list_of_values[1]
    ei = 0
    for i in range(2, t.size):
        e = r[i - 1] - y[i - 1]
        ei = ei + e
        u[i] = Kp * e + Ki * ei * ts
        y[i] = M.dot(np.array([y[i - 1], y[i - 2], u[i], u[i - 1], u[i - 2]]).transpose())
    return math.sqrt(np.sum(np.square(r - y)) / t.size)


def dummy_function(list_of_values):
    import random

    # Sometimes throws StopIteration
    if random.random() < 0.05:
        raise StopIteration

    # But usually returns: x^2 + 3x +7
    x = list_of_values[0]
    return x * x + x * 3 + 7


def ask_via_usb(list_of_values):
    import pyb.src.port as port
    port.VCP.attach('operator', list_of_values)
    port.VCP.attach('type', 9)

    data = port.VCP.read()
    while data['type'] == 0:
        data = port.VCP.read()

    if data['type'] == 9:
        return data['fitness']
    else:
        port.VCP.unread(data)
        raise StopIteration


def simple_fit_func(list_of_values):
    return (list_of_values[0] - 1.0) * (list_of_values[0] - 1.0)
