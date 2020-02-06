#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
main()
{
	supervisorctl -c $STESTS_PATH_OPS/config/supervisord.conf status all
}

# Invoke entry point.
main
