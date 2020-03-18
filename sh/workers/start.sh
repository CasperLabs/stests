#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{	
	source $STESTS_PATH_SH/workers/reset_logs.sh
	pushd $STESTS_HOME
	pipenv run supervisord -c $STESTS_PATH_OPS/config/supervisord.conf
	popd $STESTS_HOME
	log "workers :: launched supervisord"

	sleep 3.0
	source $STESTS_PATH_SH/workers/status.sh
}

# Invoke entry point.
main
