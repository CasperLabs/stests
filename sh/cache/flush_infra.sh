#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    redis-cli -n 1 --scan --pattern '*' | xargs redis-cli del
    log "CACHE :: infrastructure cache partition has been successfully flushed"
}

# Invoke entry point.
main
