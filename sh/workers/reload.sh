#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
	source $STESTS_PATH_SH/workers/stop.sh
	source $STESTS_PATH_SH/workers/run.sh
}

# Invoke entry point.
main
