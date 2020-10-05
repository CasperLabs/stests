# ###############################################################
# Helper function
# ###############################################################
function _exec_cmd()
{
    # Destructure command script & args.
    args=($@)
    args_len=${#args[@]}
    s_path=${args[0]}
    s_args=${args[@]:1:$args_len}

    # Execute script.
    pushd $STESTS_HOME
    pipenv run python3 $s_path $s_args
    popd -1
}

# ###############################################################
# ALIASES: stack 
# ###############################################################

alias stests-stack-update=$STESTS_PATH_SH/stack/update.sh                                             
alias stests-stack-vars=$STESTS_PATH_SH/stack/view_vars.sh

# ###############################################################
# ALIASES: interactive
# ###############################################################

alias stests-interactive='$STESTS_PATH_SH/workers/interactive.sh unified'
# alias stests-interactive-monitoring='$STESTS_PATH_SH/workers/interactive.sh monitoring'               # TODO: reinstate when monitoring is reactivated
# alias stests-interactive-orchestration='$STESTS_PATH_SH/workers/interactive.sh orchestration'         # TODO: reinstate when monitoring is reactivated

# ###############################################################
# ALIASES: workers
# ###############################################################

alias stests-workers=$STESTS_PATH_SH/workers/start.sh
alias stests-workers-reload=$STESTS_PATH_SH/workers/reload.sh
alias stests-workers-restart=$STESTS_PATH_SH/workers/restart.sh
alias stests-workers-start=$STESTS_PATH_SH/workers/start.sh
alias stests-workers-status=$STESTS_PATH_SH/workers/status.sh
alias stests-workers-stop=$STESTS_PATH_SH/workers/stop.sh

# ###############################################################
# ALIASES: registration
# ###############################################################

alias stests-register-lrt='$STESTS_PATH_SH/cache/register_lrt.sh'
alias stests-register-nctl='$STESTS_PATH_SH/cache/register_nctl.sh'

# ###############################################################
# ALIASES: cache
# ###############################################################

alias stests-cache-flush='$STESTS_PATH_SH/cache/flush.sh'
alias stests-cache-flush-infra='$STESTS_PATH_SH/cache/flush_infra.sh'

alias stests-cache-set-bonding-key='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_bonding_key.py'
alias stests-cache-set-faucet-key='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_faucet_key.py'
alias stests-cache-set-network='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_network.py'
alias stests-cache-set-network-status='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_network_status.py'
alias stests-cache-set-node='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_node.py'
alias stests-cache-set-node-status='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_node_status.py'

alias stests-cache-view-bonding-key='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_bonding_key.py'
# alias stests-cache-view-contracts='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_contracts.py'                     # TODO: reinstate when client is updated
alias stests-cache-view-faucet-key='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_faucet_key.py'
alias stests-cache-view-networks='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_networks.py'
alias stests-cache-view-nodes='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_nodes.py'
alias stests-cache-view-run='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_run.py'
alias stests-cache-view-run-deploys='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_run_deploys.py'
alias stests-cache-view-runs='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_view_runs.py'

# ###############################################################
# ALIASES: chain
# ###############################################################

# alias stests-chain-set-contracts='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_set_contracts.py'                       # TODO: reinstate when client is updated
# alias stests-chain-view-account-balance='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_view_account_balance.py'         # TODO: reinstate when client is updated
# alias stests-chain-view-account-id='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_view_account_id.py'                   # TODO: reinstate when client is updated
# alias stests-chain-view-account-info='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_view_account_info.py'               # TODO: reinstate when client is updated
# alias stests-chain-view-block-info='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_view_block_info.py'                   # TODO: reinstate when client is updated
# alias stests-chain-view-deploy-info='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_view_deploy_info.py'                 # TODO: reinstate when client is updated
# alias stests-chain-view-faucet-balance='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_view_faucet_balance.py'           # TODO: reinstate when client is updated

# ###############################################################
# ALIASES: generators
# ###############################################################

function _exec_generator()
{
    # Destructure generator type & args.
    args=($@)
    args_len=${#args[@]}
    g_type=${args[0]}
    g_args=${args[@]:1:$args_len}

    # Execute generator.
    _exec_cmd $STESTS_PATH_GENERATORS/wg_$g_type $g_args
}

# WG-100: Token transfer - invoked directly, i.e. wasm-less.
alias stests-wg-100='_exec_generator 100'

# WG-110: Token transfer - wasm dispatched per deploy.
alias stests-wg-110='_exec_generator 110'
