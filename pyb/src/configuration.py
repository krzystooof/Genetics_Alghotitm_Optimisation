"""
This file only contains cofiguration class
"""
import json


class Configuration:
"""
    Make a comment here
"""

    def load_file_1(self):
        data = {
            'members_to_mutate': '1',
            'member_list': '',
            'population_size': '100',
            'population_discard': '10',
            'noise': '10',
            'generation': '10',
            'total_mutations': '10',
            'random_fill': '10',
            'prev_best_fitness': '10'
        }
        # writing
        with open('data/sample_input_1.json', 'w') as outfile:
            json.dump(data, outfile)
        # reading
        with open('data/sample_input_1.json') as json_file:
            data = json.load(json_file)
            for p in data.items():
                print(p)
            members_to_mutate = data['members_to_mutate']
            print(members_to_mutate)

    def load_file_2(self):
        data = {
            'members_to_mutate': '1',
            'member_list': '',
            'population_size': '100',
            'population_discard': '10',
            'noise': '10',
            'generation': '10',
            'total_mutations': '10',
            'random_fill': '10',
            'prev_best_fitness': '10'
        }
        # writing
        with open('data/sample_input_3.json', 'w') as outfile:
            json.dump(data, outfile)
        # reading
        with open('data/sample_input_3.json') as json_file:
            data = json.load(json_file)
            for p in data.items():
                print(p)
            members_to_mutate = data['members_to_mutate']
            print(members_to_mutate)

    def load_file_3(self):
        data = {
            'members_to_mutate': '1',
            'member_list': '',
            'population_size': '100',
            'population_discard': '10',
            'noise': '10',
            'generation': '10',
            'total_mutations': '10',
            'random_fill': '10',
            'prev_best_fitness': '10'
        }
        # writing
        with open('data/sample_input_2.json', 'w') as outfile:
            json.dump(data, outfile)
        # reading
        with open('data/sample_input_2.json') as json_file:
            data = json.load(json_file)
            for p in data.items():
                print(p)
            members_to_mutate = data['members_to_mutate']
            print(members_to_mutate)


