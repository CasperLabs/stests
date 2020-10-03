#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    # Flush partition: locks.
    source $STESTS_PATH_SH/cache/flush_partition.sh 2
}

# Invoke entry point.
main
