#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf stop all &>/dev/null 
	supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf shutdown &>/dev/null
	log "workers  :: killed daemon"
}

# Invoke entry point.
main
