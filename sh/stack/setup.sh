#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
main()
{
    log "stack setup :: starts ..."

    setup_env_vars
    setup_python

    log "stack setup :: complete"
}

# Setup environment vars.
setup_env_vars()
{
    cp $STESTS_PATH_TEMPLATES/stests_vars.sh $STESTS_PATH_VARS
    . $STESTS_PATH_VARS
    log "stack setup :: env vars file --> "$STESTS_PATH_VARS 
}

# Setup python executable.
setup_python()
{
    cd $STESTS_HOME
    pipenv sync
    log "stack setup :: python venv setup"
}

# Invoke entry point.
main
