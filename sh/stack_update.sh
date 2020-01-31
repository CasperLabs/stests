#!/bin/bash

# Import utils.
source $STESTS_SH/utils.sh

# Main entry point.
main()
{
    log "stack update :: starts ..."

    update_source

    log "stack update :: complete"
}

# Update source code.
update_source()
{
    log "stack update :: pull repo updates"
    cd $STESTS_HOME
    git pull
}

# Invoke entry point.
main
