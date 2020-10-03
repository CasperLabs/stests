#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    log "workers :: logs resetting ..."
	rm $STESTS_PATH_OPS/logs/*.log
    log "workers :: logs reset"
}

# Invoke entry point.
main
