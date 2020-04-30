#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    if [ $1 = "unified" ]; then
        worker_path=$STESTS_HOME/stests
    elif [ $1 = "monitoring" ]; then
        worker_path=$STESTS_HOME/stests/monitoring
    elif [ $1 = "workflows" ]; then
        worker_path=$STESTS_HOME/stests/workflows
    fi

    cd $STESTS_HOME
	pipenv run dramatiq worker --path $worker_path --watch $STESTS_PATH_SRC
}

# Invoke entry point.
main $1
