#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    # Flush partition: infra.
    source $STESTS_PATH_SH/cache/flush_partition.sh 1

    log "Cache successfully flushed"
}

# Invoke entry point.
main
