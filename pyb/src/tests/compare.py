import json

# with open('results_octave.json') as octave_results:
# f = open(r'C:\Users\Gregori\Desktop\Zmienna_X.txt', "r")
f = open(r'results_octave.txt', "r")
with open('results.json') as algorithm_results:
    final_result_algorithm = 0
    final_result_octave = 0
    result_algorithm = json.load(algorithm_results)
    for p in result_algorithm.items():
        final_result_algorithm = result_algorithm['gen10']
    final_result_algorithm[0] = float(final_result_algorithm[0])
    final_result_algorithm[1] = float(final_result_algorithm[1])
    f.readline()
    f.readline()
    f.readline()
    final_result_octave = f.readline()
    print(final_result_octave)
    final_result_octave = float(final_result_octave)
    print(final_result_algorithm)
    assert final_result_octave == final_result_algorithm[0]
