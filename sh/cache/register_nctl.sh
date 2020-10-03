#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    log "nctl :: registering assets ..."

    # Flush cache.
    source $STESTS_PATH_SH/cache/flush.sh
    source $STESTS_PATH_SH/cache/flush_infra.sh

    pushd $STESTS_HOME
    pipenv run python3 $STESTS_PATH_SH_SCRIPTS/cache_register_nctl.py
    popd -1    

    log "nctl :: registered assets"
}

# Invoke entry point.
main
