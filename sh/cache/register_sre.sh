#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    # Flush cache.
    source $STESTS_PATH_SH/cache/flush.sh
    source $STESTS_PATH_SH/cache/flush_infra.sh

    pushd $STESTS_HOME
    pipenv run python $STESTS_PATH_SH_SCRIPTS/cache_register_sre.py
    popd -1    
}

# Invoke entry point.
main