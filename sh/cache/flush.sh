#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    source $STESTS_PATH_SH/cache/flush_infra.sh
    source $STESTS_PATH_SH/cache/flush_monitoring.sh
    source $STESTS_PATH_SH/cache/flush_run.sh
}

# Invoke entry point.
main
