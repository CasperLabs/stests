#!/bin/bash

# Import utils.
source $STESTS_SH/utils.sh

# Main entry point.
main()
{
	source $STESTS_SH/workers_reset_logs.sh
	supervisord -c $STESTS_OPS/config/supervisord.conf
	log "workers start :: launched supervisord"

	sleep 3.0
	source $STESTS_SH/workers_status.sh
}

# Invoke entry point.
main
