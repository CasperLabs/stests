#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	# Escape if already running interactively.
	interactive_socket=$STESTS_PATH_OPS/daemon/interactive.sock
    if [ -e $interactive_socket ]; then
        log "stests is already running in interactive mode:"
        log "- if the socket file ($interactive_socket) is stale then clear it and retry,"
		exit 0
    fi
	interactive_socket=$STESTS_PATH_OPS/daemon/interactive-monitoring.sock
    if [ -e $interactive_socket ]; then
        log "stests is already running in interactive mode:"
        log "- if the socket file ($interactive_socket) is stale then clear it and retry,"
		exit 0
    fi
	interactive_socket=$STESTS_PATH_OPS/daemon/interactive-workflows.sock
    if [ -e $interactive_socket ]; then
        log "stests is already running in interactive mode:"
        log "- if the socket file ($interactive_socket) is stale then clear it and retry,"
		exit 0
    fi

	# Reset logs.
	source $STESTS_PATH_SH/workers/reset_logs.sh

	# Reset locks.
	source $STESTS_PATH_SH/cache/flush_locks.sh

	# Launch daemon.
	pushd $STESTS_HOME
	pipenv run supervisord -c $STESTS_PATH_OPS/config/supervisord.conf
	popd -1
	log "workers :: launched supervisord"
	
	# Wait for daemon to start and display status.
	sleep 3.0
	source $STESTS_PATH_SH/workers/status.sh
}

# Invoke entry point.
main
