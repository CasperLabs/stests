#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
main()
{
	source $STESTS_PATH_SH/workers_reset_logs.sh
	supervisord -c $STESTS_PATH_OPS/config/supervisord.conf
	log "workers start :: launched supervisord"

	sleep 3.0
	source $STESTS_PATH_SH/workers_status.sh
}

# Invoke entry point.
main
