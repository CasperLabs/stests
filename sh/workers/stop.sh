#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	log "workers  :: daemon stopping ..."
	pushd $STESTS_HOME
	pipenv run supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf stop all &>/dev/null 
	pipenv run supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf shutdown &>/dev/null
	popd -1
	log "workers  :: daemon stopped"
}

# Invoke entry point.
main
