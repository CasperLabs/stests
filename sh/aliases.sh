# ###############################################################
# ALIASES: stack 
# ###############################################################

# Stack commands.
alias stests-stack-install=$STESTS_SH/sh/stack_install.sh
alias stests-stack-update=$STESTS_SH/sh/stack_update.sh

# ###############################################################
# ALIASES: workers
# ###############################################################

# Workers commands.
alias stests-workers=$STESTS_SH/workers_start.sh
alias stests-workers-stop=$STESTS_SH/workers_stop.sh
alias stests-workers-reload=$STESTS_SH/workers_reload.sh
alias stests-workers-status=$STESTS_SH/workers_status.sh
alias stests-workers-reset-logs=$STESTS_SH/workers_reset_logs.sh

# ###############################################################
# ALIASES: cache
# ###############################################################

# Cache interaction commands.
alias stests-cache-set-network='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_network.py'
alias stests-cache-set-node='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_node.py'
alias stests-cache-set-node-bonding-key='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_node_bonding_key.py'
