#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    cd $STESTS_HOME
    pipenv run dramatiq -p 1 -t 4 worker --path $STESTS_HOME $STESTS_PATH_SRC --watch $STESTS_PATH_SRC
}

# Invoke entry point.
main