#!/bin/bash

# Import utils.
source $STESTS_PATH_SH/utils.sh

# Main entry point.
function main()
{
    printenv | grep STESTS_ | sort
}

# Invoke entry point.
main
