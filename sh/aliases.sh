# ###############################################################
# ALIASES: stack 
# ###############################################################

# Stack commands.
alias stests-stack-setup=$STESTS_SH/stack_setup.sh
alias stests-stack-update=$STESTS_SH/stack_update.sh

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
alias stests-set-network='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_network.py'
alias stests-set-network-faucet-key='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_network_faucet_key.py'
alias stests-set-node='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_node.py'
alias stests-set-node-bonding-key='cd $STESTS_HOME && pipenv run python $STESTS_CLI/cache/set_node_bonding_key.py'

# ###############################################################
# ALIASES: generators
# ###############################################################

_exec_generator()
{
    # Destructure generator type, pahse & args.
    args=($@)
    args_len=${#args[@]}
    g_type=${args[0]}
    g_phase=${args[1]}
    g_args=${args[@]:2:$args_len}

    # Execute generator.
    pipenv run python $STESTS_GENERATORS/wg_$g_type/phase_$g_phase $g_args
}

# WG-100: ERC-20 auction.
alias stests-wg-100-phase-01='_exec_generator 100 01'
