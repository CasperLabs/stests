#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    log "cache :: flushing infra ..."
    source $STESTS_PATH_SH/cache/flush_partition.sh 1
    log "cache :: flushed infra"
}

# Invoke entry point.
main
