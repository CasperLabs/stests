#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	pushd $STESTS_HOME
	pipenv run supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf stop all &>/dev/null 
	pipenv run supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf shutdown &>/dev/null
	popd $STESTS_HOME
	log "workers  :: killed daemon"
}

# Invoke entry point.
main
