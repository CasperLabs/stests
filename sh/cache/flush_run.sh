#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    redis-cli -p $STESTS_CACHE_REDIS_PORT -n 3 --scan --pattern '*' | xargs redis-cli -p $STESTS_CACHE_REDIS_PORT del
    log "CACHE :: run cache partition has been successfully flushed"
}

# Invoke entry point.
main
