#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    redis-cli -n 0 --scan --pattern '*' | xargs redis-cli del
    log "MQ :: redis broker successfully flushed"
}

# Invoke entry point.
main
