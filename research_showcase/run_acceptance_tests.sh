#!/bin/bash

# Ensure we are in the correct directory (research_showcase)
cd "$(dirname "$0")"

# Install/update required packages (optional, assuming venv is active)
# echo "Ensuring acceptance test dependencies are installed..."
# ./venv/bin/python -m pip install -r requirements.txt > /dev/null

# Check if pytest is available in the virtual environment
if ! ./venv/bin/pytest --version > /dev/null 2>&1; then
    echo "Error: pytest not found in virtual environment. Please ensure dependencies are installed."
    exit 1
fi

# Run acceptance tests with HTML report
echo "Running acceptance tests..."

# Default arguments
PYTEST_ARGS="-v --django-debug-mode --html=acceptance_tests/acceptance_report.html --self-contained-html -m acceptance"

# Check for --headless argument passed to this script
if [[ " $@ " =~ " --headless " ]]; then
  echo "Running in headless mode."
  PYTEST_ARGS="$PYTEST_ARGS --headless"
fi

# Execute pytest from the virtual environment
./venv/bin/pytest $PYTEST_ARGS acceptance_tests/test_submission.py
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Acceptance tests completed successfully."
    echo "HTML report available at: acceptance_tests/acceptance_report.html"
elif [ $EXIT_CODE -eq 5 ]; then
    echo "Acceptance tests completed, but no tests marked with 'acceptance' were found."
else
    echo "Acceptance tests failed with exit code $EXIT_CODE."
    echo "HTML report (if generated) available at: acceptance_tests/acceptance_report.html"
fi

exit $EXIT_CODE 