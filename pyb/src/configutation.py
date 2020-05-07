"""
File contains creating variables for algorithm to work.

Class used to set parameters in algorithm to work. It also reads and writes parameters into file.
@author: Grzegorz Drozda
"""

import json


class Configuration:

    @staticmethod
    def load_file_1():
        """Setting variables for algorithm"""
        data = {
            'operator': '1',
            'population_size': '100',
            'population_discard': '10',
            'noise': '10',
            'mutation_options': '10',
            'crossover_options': '10'
        }
        """Writing parameters into file"""
        with open('data/sample_input_1.json', 'w') as outfile:
            json.dump(data, outfile)
        """Reading parameters from file"""
        with open('data/sample_input_1.json') as json_file:
            data = json.load(json_file)
            # for p in data.items():
            #     print(p)
            # operator = data['operator']
            # print(operator)

    def load_file_2(self):
        """Setting variables for algorithm"""
        data = {
            'operator': '1',
            'population_size': '100',
            'population_discard': '10',
            'noise': '10',
            'mutation_options': '10',
            'crossover_options': '10'
        }
        """Writing parameters into file"""
        with open('data/sample_input_3.json', 'w') as outfile:
            json.dump(data, outfile)
        """Reading parameters from file"""
        with open('data/sample_input_3.json') as json_file:
            data = json.load(json_file)
            # for p in data.items():
            #     print(p)
            # operator = data['operator']
            # print(operator)

    def load_file_3(self):
        """Setting variables for algorithm"""
        data = {
            'operator': '1',
            'population_size': '100',
            'population_discard': '10',
            'noise': '10',
            'mutation_options': '10',
            'crossover_options': '10'
        }
        """Writing parameters into file"""
        with open('data/sample_input_2.json', 'w') as outfile:
            json.dump(data, outfile)
        """Reading parameters into file"""
        with open('data/sample_input_2.json') as json_file:
            data = json.load(json_file)
            # for p in data.items():
            #     print(p)
            # operator = data['operator']
            # print(operator)
