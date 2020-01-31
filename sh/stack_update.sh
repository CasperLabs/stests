#!/bin/bash

# Import utils.
source $STESTS_SH/utils.sh

# Main entry point.
main()
{
    log "stack update :: starts ..."

    # update_source
    update_env_vars

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
	if [ -f $HOME/.stests ]; then
		declare backup=$HOME/.stests-"`date +%Y-%m-%d`"
		cp $HOME/.stests $backup
		log "stack update :: env vars file backup --> "$backup
	fi

    cp $STESTS_TEMPLATES/stests_env.sh $HOME/.stests
    log "stack update :: new env vars file --> "$HOME/.stests
}

# Invoke entry point.
main
