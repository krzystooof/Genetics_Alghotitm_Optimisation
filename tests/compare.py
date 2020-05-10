import json


with open('algorithm_results.json') as algorithm:
    with open(r'results_octave.txt', "r") as octave:
        algorithm_results = json.load(algorithm)['calculated_result']

        final_from_algorithm = float(algorithm_results[0])
        final_from_octave = float(octave.readlines()[3])

        print("Octave results: ", final_from_octave)
        print("PTMAG results: ", final_from_algorithm)

        tolerance = 0.05

        assert (final_from_algorithm >= final_from_octave - tolerance) and (
                final_from_algorithm <= final_from_octave + tolerance)
