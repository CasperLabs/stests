#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    # Escape if daemon is already running.
    daemon_socket=$STESTS_PATH_OPS/daemon/supervisord.sock
    if [ -e "$daemon_socket" ]; then
        log "stests workers are running in daemon mode:"
        log "- if the socket file ($daemon_socket) is stale then clear it and retry,"
        log "- otherwise stop the workers (stests-workers-stop) and retry."
        exit 0
    fi

    # Mock a socket file to protect against repeatedly running in interactive mode.
    if [ $1 = "unified" ]; then
        interactive_socket=$STESTS_PATH_OPS/daemon/interactive.sock
    else
        interactive_socket=$STESTS_PATH_OPS/daemon/interactive-$1.sock
    fi
    if [ -e "$interactive_socket" ]; then
        log "stests is already running in interactive mode:"
        log "- if the socket file ($interactive_socket) is stale then clear it and retry,"
        exit 0
    fi
    touch $interactive_socket

    # Switch worker depending upon mode.
    worker_path=$STESTS_HOME/stests/workers
    cd $STESTS_HOME
    if [ $1 = "unified" ]; then
        source $STESTS_PATH_SH/cache/flush_locks.sh
        pipenv run dramatiq interactive_0 --path $worker_path --watch $STESTS_PATH_SRC
    elif [ $1 = "monitoring" ]; then
        source $STESTS_PATH_SH/cache/flush_locks.sh
        pipenv run dramatiq interactive_1 --path $worker_path --watch $STESTS_PATH_SRC
    elif [ $1 = "orchestration" ]; then
        pipenv run dramatiq interactive_2 --path $worker_path --watch $STESTS_PATH_SRC
    fi

    # Tidy up.
    rm $interactive_socket
}

# Invoke entry point.
main $1
