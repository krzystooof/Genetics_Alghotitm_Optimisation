with open('results_octave.json') as octave_results:
    with open('algorithm_results.json') as algorithm_results:
        assert algorithm_results == octave_results
