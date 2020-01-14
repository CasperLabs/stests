#!/bin/bash -e

# Initialise test run arguments.
if [[ "$TEST_RUN_ARGS" == "" ]]; then
    TEST_RUN_ARGS=$@
fi

# Run tests.
pipenv run tox $TEST_RUN_ARGS
