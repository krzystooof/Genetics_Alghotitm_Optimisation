from pyb.src.algorithm import Population
import json

import math
import numpy as np
import matplotlib.pyplot as plt

def main():
    config = get_config()
    population = Population(config)

    while population.generation < 1000:  # TODO find good break condition
        for member in population.member_list:
            member.fitness = get_fitness(member.operator)
        population.new_gen()

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


def get_config():
    mutate = [1, 2, 3, 4]
    crossover = [1, 2]
    config_dict = {
        'generations': 1000,
        'population_size': 100,
        'population_discard': 0.5,
        'population_noise': 0.1,
        'population_chance_bonus': 2,
        'population_reverse_fitness': True,
        'member_config': {
            'random_low': -100,
            'random_high': 100,
            'num_values': 2,
            'mutation_options': mutate,
            'crossover_options': crossover
            }

    }
    return config_dict

minimum = 10000
maximum = 0.0
counter = 0

def get_fitness(operator):  # simpleFitFunc, but in python
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

    # plot results - disable for optimization !!!
    # fig = plt.figure()
    # ax = fig.gca()
    # ax.grid(True)
    # ax.set_ylabel('Output signal [-]')
    # ax.set_xlabel('Time [s]')
    # plt.plot(t, y)
    # plt.show()
    global minimum
    global maximum
    if q < minimum:
        minimum = q
    if q > maximum:
        maximum = q
    print(q)
    print("Minimum: ", minimum)
    print("Maximum: ", maximum)
    global counter
    counter = counter + 1
    print("Counter: ", counter)
    return q

main()