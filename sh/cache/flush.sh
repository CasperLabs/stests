#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    log "cache :: flushing"

    # Flush partition: broker.
    source $STESTS_PATH_SH/cache/flush_partition.sh 0

    # Flush partition: monitoring locks.
    source $STESTS_PATH_SH/cache/flush_locks.sh

    # Flush partition: monitoring data.
    source $STESTS_PATH_SH/cache/flush_partition.sh 3

    # Flush partition: orchestration locks.
    source $STESTS_PATH_SH/cache/flush_partition.sh 4

    # Flush partition: orchestration data.
    source $STESTS_PATH_SH/cache/flush_partition.sh 5

    # Flush partition: workflow data.
    source $STESTS_PATH_SH/cache/flush_partition.sh 6

    log "cache :: flushed"
}

# Invoke entry point.
main
