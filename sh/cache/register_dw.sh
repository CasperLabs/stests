#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    log "sre :: registering dw assets ..."

    # Flush cache.
    source $STESTS_PATH_SH/cache/flush.sh
    source $STESTS_PATH_SH/cache/flush_infra.sh

    pushd $STESTS_HOME
    pipenv run python3 $STESTS_PATH_SH_SCRIPTS/cache_register_dw.py --assets $1
    popd -1    

    log "sre :: registered dw assets"
}

# Invoke entry point.
main $1
