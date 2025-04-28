#!/bin/bash

# Run acceptance tests with options for visibility and reporting
echo "Running acceptance tests..."

# Options / Flags
REQUEST_VISIBLE=false # Default to headless unless --visible is passed
HTML_REPORT_FLAG=false
SPECIFIC_TEST=""

# Process arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --visible)
            REQUEST_VISIBLE=true
            echo "Requesting visible mode (browser should be displayed)"
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

# Build base pytest command arguments
PYTEST_BASE_ARGS=("-v")
# Add --headless only if --visible was NOT requested
if [[ "$REQUEST_VISIBLE" == false ]]; then
    echo "--visible not specified, adding --headless flag for pytest."
    PYTEST_BASE_ARGS+=("--headless")
fi

# Determine target and run tests
if [[ -n "$SPECIFIC_TEST" ]]; then
    echo "Running specific test file: acceptance_tests/$SPECIFIC_TEST"
    TARGET="acceptance_tests/$SPECIFIC_TEST"
    python -m pytest "${PYTEST_BASE_ARGS[@]}" "$TARGET"
    EXIT_CODE=$?
else
    # Run all acceptance tests marked with 'acceptance'
    echo "Running all acceptance tests (marked with 'acceptance')..."
    TARGET="acceptance_tests/"
    python -m pytest "${PYTEST_BASE_ARGS[@]}" "$TARGET" -m acceptance
    EXIT_CODE=$?
fi

# Generate an HTML report if requested
if [[ "$HTML_REPORT_FLAG" == true ]]; then
    echo "Generating HTML report..."

    # Build HTML reporting command arguments
    HTML_ARGS=("${PYTEST_BASE_ARGS[@]}" "--html=acceptance_report.html" "--self-contained-html")

    # Rerun tests with HTML reporting enabled
    # Note: This reruns the tests.
    if [[ -n "$SPECIFIC_TEST" ]]; then
        python -m pytest "${HTML_ARGS[@]}" "$TARGET"
    else
        python -m pytest "${HTML_ARGS[@]}" "$TARGET" -m acceptance
    fi
    if [[ $? -eq 0 ]]; then
        echo "HTML report available at: acceptance_report.html"
    else
        echo "Warning: HTML report generation failed or tests failed during report generation."
    fi
fi

echo "Tests completed with exit code: $EXIT_CODE."
exit $EXIT_CODE 