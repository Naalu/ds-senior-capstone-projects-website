#!/bin/bash

# Run acceptance tests with options for visibility and reporting
echo "Running acceptance tests..."

# Default to running in headless mode
HEADLESS="--headless"
HTML_REPORT_FLAG=false
SPECIFIC_TEST=""

# Process arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --visible)
            HEADLESS=""
            echo "Running in visible mode (browser will be displayed)"
            shift # past argument
            ;;
        --html)
            HTML_REPORT_FLAG=true
            shift # past argument
            ;;
        -*|--*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            # Assume non-option argument is the specific test file
            if [[ -z "$SPECIFIC_TEST" ]]; then
                SPECIFIC_TEST="$1"
            else
                 echo "Error: Multiple test files specified: $SPECIFIC_TEST and $1"
                 exit 1
            fi
            shift # past argument or value
            ;;
    esac
done

# Navigate to the project directory (where the script is located)
cd "$(dirname "$0")"

PYTEST_CMD="python -m pytest -v $HEADLESS"

# Determine what to run
if [[ -n "$SPECIFIC_TEST" ]]; then
    echo "Running specific test file: acceptance_tests/$SPECIFIC_TEST"
    TARGET="acceptance_tests/$SPECIFIC_TEST"
    $PYTEST_CMD $TARGET
    EXIT_CODE=$?
else
    # Run all acceptance tests marked with 'acceptance'
    echo "Running all acceptance tests (marked with 'acceptance')..."
    TARGET="acceptance_tests/"
    $PYTEST_CMD $TARGET -m acceptance
    EXIT_CODE=$?
fi

# Generate an HTML report if requested
if [[ "$HTML_REPORT_FLAG" == true ]]; then
    echo "Generating HTML report..."
    # Rerun tests with HTML reporting enabled
    # Note: This reruns the tests. If only report generation is needed after a run,
    #       a different approach (like pytest-cache) might be explored.
    HTML_CMD="python -m pytest -v $HEADLESS --html=acceptance_report.html --self-contained-html"
    if [[ -n "$SPECIFIC_TEST" ]]; then
        $HTML_CMD $TARGET
    else
        $HTML_CMD $TARGET -m acceptance
    fi
    if [[ $? -eq 0 ]]; then
        echo "HTML report available at: acceptance_report.html"
    else
        echo "Warning: HTML report generation failed or tests failed during report generation."
    fi
fi

echo "Tests completed with exit code: $EXIT_CODE."
exit $EXIT_CODE 