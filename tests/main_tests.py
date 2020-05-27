# This file will not exist, Algorithm class will take care of it

from pyb.src.algorithm_core import Population
from pyb.src.algorithm_core import Config
import json

import math
import numpy as np
import matplotlib.pyplot as plt


def main():
    population = Population(Config(noise=0.7, reverse=True, num_values=2))
    for member in population.member_list:
        member.fitness = get_fitness(member.operator)

    while population.generation < 100:  # TODO break condition dependent on accuarcy
        population.new_gen()

        for member in population.member_list:
            member.fitness = get_fitness(member.operator)
        population.update_stats()
        print("Best member's fitness: ", population.best_member.fitness)
        print("Best member's operator: ", population.best_member.operator.values)
        print("Generation:", population.generation)

    for member in population.member_list:
        member.fitness = get_fitness(member.operator)
    population.update_stats()
    print("Best member's fitness: ", population.best_member.fitness)
    print("Best member's operator: ", population.best_member.operator.values)

    # Saving final results into json
    final_results = {
        'calculated_result': population.best_member.operator.values,
    }
    with open("algorithm_results.json", "w") as write_file:
        json.dump(final_results, write_file)



# TODO import get_fitness from sample_functions.py
# don't comment \/ this \/. Code above needs it
def get_fitness(operator):  # not simple FitFunc, but in python
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

main()