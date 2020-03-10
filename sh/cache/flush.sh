#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    redis-cli -h $STESTS_CACHE_REDIS_HOST -p $STESTS_CACHE_REDIS_PORT FLUSHALL
}

# Invoke entry point.
main
