#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    worker_path=$STESTS_HOME/stests/workers
    cd $STESTS_HOME
    if [ $1 = "unified" ]; then
        pipenv run dramatiq interactive_0 --path $worker_path --watch $STESTS_PATH_SRC
    elif [ $1 = "monitoring" ]; then
        pipenv run dramatiq interactive_1 --path $worker_path --watch $STESTS_PATH_SRC
    elif [ $1 = "workflows" ]; then
        pipenv run dramatiq interactive_2 --path $worker_path --watch $STESTS_PATH_SRC
    fi
}

# Invoke entry point.
main $1
