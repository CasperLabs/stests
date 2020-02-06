#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
main()
{
	supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf stop all
	supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf shutdown
	log "workers stop :: killed daemon"
}

# Invoke entry point.
main
