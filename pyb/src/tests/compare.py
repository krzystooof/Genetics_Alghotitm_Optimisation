with open('results_octave.json') as octave_results:
    with open('results.json') as algorithm_results:
        assert octave_results == algorithm_results
