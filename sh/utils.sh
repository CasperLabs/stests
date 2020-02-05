#!/bin/bash

# ###############################################################
# UTILS: constants
# ###############################################################

export STESTS_PYTHON_VERSION=3.8.1

# ###############################################################
# UTILS: helper functions
# ###############################################################

# Wraps standard echo by adding application prefix.
log()
{
    # Set timestamp.
	declare now=`date +%Y-%m-%dT%H:%M:%S:000000`

    # Support tabs.
	declare tabs=''

    # Emit log message.
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				declare tabs+='\t'
			done
	    	echo -e $now" [INFO] :: CL-STESTS :: "$tabs$1
	    else
	    	echo -e $now" [INFO] :: CL-STESTS :: "$1
	    fi
	else
	    echo -e $now" [INFO] :: CL-STESTS :: "
	fi
}
