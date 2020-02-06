#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    log "workers :: resetting logs ..."

	rm $STESTS_PATH_OPS/logs/*.log

    # TODO
}

# Invoke entry point.
main
