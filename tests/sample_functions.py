def test_1(operator):  # TODO: find relevant name
    # TODO test for this function
    import numpy as np
    import math

    # model
    M = np.array([1.995908286, -0.996008084, 0.000024949, 0.000049899, 0.000024949])

    # simulation time
    tsim = 30  # [s]

    # sample time
    ts = 0.01  # [s]

    # time vector
    t = np.arange(0, tsim, ts)  # [s]

    # model output signal
    y = np.zeros(t.size)

    # model input signal
    u = np.zeros(t.size)

    # model reference signal
    r = np.ones(t.size)

    # controller gains
    Kp = operator.values[0]
    Ki = operator.values[1]
    ei = 0

    # simulation loop
    for i in range(2, t.size):
        e = r[i - 1] - y[i - 1]
        ei = ei + e
        u[i] = Kp * e + Ki * ei * ts
        y[i] = M.dot(np.array([y[i - 1], y[i - 2], u[i], u[i - 1], u[i - 2]]).transpose())

    q = math.sqrt(np.sum(np.square(r - y)) / t.size)
    return q


def sample_function(list_of_values):
    import random

    # Sometimes throws StopIteration
    if random.random() < 0.05:
        raise StopIteration

    # But usually returns: x^2 + 3x +7
    x = list_of_values[0]
    return x * x + x * 3 + 7
