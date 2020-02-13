#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	source $STESTS_PATH_SH/workers/stop.sh
	source $STESTS_PATH_SH/workers/start.sh
}

# Invoke entry point.
main
