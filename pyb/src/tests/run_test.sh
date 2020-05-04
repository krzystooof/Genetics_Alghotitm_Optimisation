#!/bin/bash
octave-cli "ga_example.m" > results_octave.json
# Run alogrithm, create another results

python "../main.py" > results.json
python compare.py # Exec asserts
