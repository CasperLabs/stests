#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
main()
{
    log "stack update :: starts ..."

    update_source
    update_env_vars
    update_venv

    log "stack update :: complete"
}

# Update source code.
update_source()
{
    log "stack update :: pull repo updates"
    cd $STESTS_HOME
    git pull
}

# Update environment variables.
update_env_vars()
{
	if [ -f $STESTS_PATH_VARS ]; then
		declare backup=$STESTS_PATH_VARS-"`date +%Y-%m-%d`"
		cp $STESTS_PATH_VARS $backup
		log "stack update :: env vars file backup --> "$backup
	fi

    cp $STESTS_PATH_TEMPLATES/stests_vars.sh $STESTS_PATH_VARS
    log "stack update :: new env vars file --> "$STESTS_PATH_VARS
}

# Update virtual environment.
update_venv()
{
    log "stack update :: updating python3 venv"
    cd $STESTS_HOME
    pipenv sync
}

# Invoke entry point.
main
