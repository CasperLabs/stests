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
    cp $STESTS_PATH_TEMPLATES/stests_env.sh $HOME/.stests
    . $HOME/.stests
    log "stack setup :: env vars file --> "$HOME/.stests 
}

# Setup python executable.
setup_python()
{
    # Install pyenv.
    curl https://pyenv.run | bash
    cat $STESTS_PATH_TEMPLATES/pyenv_completion.txt >> ~/.bashrc

    # Via pyenv, install python.
    pyenv install $STESTS_PYTHON_VERSION

    # Via pyenv, set stests local python.
    cd $STESTS_HOME
    pyenv local $STESTS_PYTHON_VERSION

    # Via pipenv, stests venv.
    pip install -U pipenv
    pipenv sync

    log "stack setup :: python venv setup"
}

# Setup daemons.
setup_daemons()
{
    log "stack setup :: TODD setup daemons ?"
}

# Invoke entry point.
main
