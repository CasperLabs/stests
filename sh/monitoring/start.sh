#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    cd $STESTS_HOME
    pipenv run python $STESTS_PATH_MONITORING
}

# Invoke entry point.
main
