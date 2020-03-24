#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	pushd $STESTS_HOME
	pipenv run supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf status all
	popd -1
}

# Invoke entry point.
main
