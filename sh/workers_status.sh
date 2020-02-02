#!/bin/bash

# Import utils.
source $STESTS_SH/utils.sh

# Main entry point.
main()
{
	supervisorctl -c $STESTS_OPS/config/supervisord.conf status all
}

# Invoke entry point.
main
