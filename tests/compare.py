import json


with open('algorithm_results.json') as algorithm:
    with open(r'results_octave.txt', "r") as octave:
        algorithm_results = json.load(algorithm)['best_fitness']

        final_from_algorithm = float(algorithm_results[0])
        final_from_octave = float(octave.readlines()[3])

        print("Octave results: ", final_from_octave)
        print("PTMAG results: ", final_from_algorithm)

        assert final_from_algorithm == final_from_octave
