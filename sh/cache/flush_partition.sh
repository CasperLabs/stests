#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    redis-cli -h $STESTS_CACHE_REDIS_HOST -p $STESTS_CACHE_REDIS_PORT -n $1 FLUSHDB >/dev/null
}

# Invoke entry point.
main $1
