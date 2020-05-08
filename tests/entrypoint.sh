#!/bin/bash
# Create octave results as reference
cd /app/tests && octave-cli ga_example.m > results_octave.json

# Run alogrithm, create another results
cd /app/pyb/src/ && python main.py

# Compare given results
cd /app/tests && python compare.py
