#!/bin/bash

# Create octave results as reference
octave-cli ga_example.m > results_octave.txt

# Run alogrithm, create another results
python main_tests.py
coverage run test_alogrithm
coverage report

# Compare given results
python compare.py
