#!/bin/bash

# Ensure we are in the correct directory (where manage.py is)
cd "$(dirname "$0")"

# Run tests with coverage
echo "Running verification tests with coverage..."
coverage run --rcfile=.coveragerc manage.py test research users

# Generate coverage reports
echo "Generating coverage reports..."
coverage report -m
coverage html

echo "Verification tests completed."
echo "HTML coverage report available at: htmlcov/index.html" 