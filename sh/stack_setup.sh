#!/bin/bash

# Import utils.
source $STESTS_SH/utils.sh

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
    cp $STESTS_TEMPLATES/stests_env.sh $HOME/.stests
    . $HOME/.stests
    log "stack setup :: env vars file --> "$HOME/.stests 
}

# Setup python executable.
setup_python()
{
    log "stack setup :: TODD setup python via pyenv and pipenv ?"
}

# Invoke entry point.
main
