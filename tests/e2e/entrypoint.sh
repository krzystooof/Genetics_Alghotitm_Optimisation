#!/bin/bash

# Create octave results as reference
octave-cli ga_example.m > results_octave.txt

# Run algorithm, implicitly create another results in json file
python run_algorithm.py

# Compare given results
python compare.py
