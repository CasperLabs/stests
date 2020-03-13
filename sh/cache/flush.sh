#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    # Flush partition: broker.
    source $STESTS_PATH_SH/cache/flush_partition.sh 0

    # Flush partition: monitoring.
    source $STESTS_PATH_SH/cache/flush_partition.sh 2

    # Flush partition: workflow engine.
    source $STESTS_PATH_SH/cache/flush_partition.sh 3

    # Flush partition: workflow data.
    source $STESTS_PATH_SH/cache/flush_partition.sh 4
}

# Invoke entry point.
main
