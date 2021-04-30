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
# ALIASES: Stack
# ###############################################################

alias stests-stack-update=$STESTS_PATH_SH/stack/update.sh
alias stests-stack-vars=$STESTS_PATH_SH/stack/view_vars.sh

# ###############################################################
# ALIASES: Interactive
# ###############################################################

alias stests-interactive='$STESTS_PATH_SH/workers/interactive.sh unified'
alias stests-interactive-monitoring='$STESTS_PATH_SH/workers/interactive.sh monitoring'
alias stests-interactive-orchestration='$STESTS_PATH_SH/workers/interactive.sh orchestration'

# ###############################################################
# ALIASES: Workers
# ###############################################################

alias stests-workers=$STESTS_PATH_SH/workers/start.sh
alias stests-workers-reload=$STESTS_PATH_SH/workers/reload.sh
alias stests-workers-restart=$STESTS_PATH_SH/workers/restart.sh
alias stests-workers-start=$STESTS_PATH_SH/workers/start.sh
alias stests-workers-status=$STESTS_PATH_SH/workers/status.sh
alias stests-workers-stop=$STESTS_PATH_SH/workers/stop.sh

# ###############################################################
# ALIASES: Nodes
# ###############################################################

alias stests-node-start='_exec_cmd $STESTS_PATH_SH_SCRIPTS/node_start.py'
alias stests-node-stop='_exec_cmd $STESTS_PATH_SH_SCRIPTS/node_stop.py'
alias stests-node-toggle='_exec_cmd $STESTS_PATH_SH_SCRIPTS/node_toggle.py'
alias stests-node-upgrade='_exec_cmd $STESTS_PATH_SH_SCRIPTS/node_upgrade.py'

# ###############################################################
# ALIASES: Registration
# ###############################################################

alias stests-register-dw='$STESTS_PATH_SH/cache/register_dw.sh'
alias stests-register-lrt='$STESTS_PATH_SH/cache/register_lrt.sh'
alias stests-register-nctl='$STESTS_PATH_SH/cache/register_nctl.sh'

# ###############################################################
# ALIASES: Cache management
# ###############################################################

alias stests-cache-flush='$STESTS_PATH_SH/cache/flush.sh'
alias stests-cache-flush-infra='$STESTS_PATH_SH/cache/flush_infra.sh'
# alias stests-chain-set-contracts='_exec_cmd $STESTS_PATH_SH_SCRIPTS/chain_set_contracts.py'                       # TODO: reinstate when client is updated
alias stests-cache-set-bonding-key='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_bonding_key.py'
alias stests-cache-set-faucet-key='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_faucet_key.py'
alias stests-cache-set-network='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_network.py'
alias stests-cache-set-network-status='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_network_status.py'
alias stests-cache-set-node='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_node.py'
alias stests-cache-set-node-status='_exec_cmd $STESTS_PATH_SH_SCRIPTS/cache_set_node_status.py'

# ###############################################################
# ALIASES: Views
# ###############################################################

# Views #1: chain.
alias stests-view-chain-account='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_account.py'
alias stests-view-chain-account-balance='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_account_balance.py'
alias stests-view-chain-account-hash='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_account_hash.py'
alias stests-view-chain-account-main-purse-uref='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_account_main_purse_uref.py'
alias stests-view-chain-auction-info='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_auction_info.py'
alias stests-view-chain-block='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_block.py'
alias stests-view-chain-deploy='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_deploy.py'
alias stests-view-chain-era='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_era.py'
alias stests-view-chain-height='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_height.py'
alias stests-view-chain-state-root-hash='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_chain_state_root_hash.py'

# Views #2: node information.
alias stests-view-node-events='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_events.py'
alias stests-view-node-metric='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py'
alias stests-view-node-metric-deploy-gossiper='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py --metric deploy_gossiper'
alias stests-view-node-metric-contract-runtime='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py --metric contract_runtime'
alias stests-view-node-metric-finalised-block-count='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py --metric amount_of_blocks'
alias stests-view-node-metric-memory='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py --metric mem_'
alias stests-view-node-metric-pending-deploy-count='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py --metric pending_deploy'
alias stests-view-node-metric-scheduler-queue='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_metric.py --metric scheduler_queue'
alias stests-view-node-peers='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_peers.py'
alias stests-view-node-status='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_node_status.py'

# Views #3: infra information.
alias stests-view-infra-networks='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_infra_networks.py'
alias stests-view-infra-nodes='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_infra_nodes.py'

# Views #4: faucet information.
alias stests-view-faucet-account='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_faucet_account.py'
alias stests-view-faucet-account-balance='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_faucet_account_balance.py'
alias stests-view-faucet-account-keys='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_faucet_account_keys.py'

# State information.
# alias stests-view-contracts='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_contracts.py'                                 # TODO: reinstate when client is updated

# Views #5: validator information.
alias stests-view-validator-account='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_validator_account.py'
alias stests-view-validator-account-balance='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_validator_account_balance.py'
alias stests-view-validator-account-keys='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_validator_account_keys.py'

# Views #6: generator information.
alias stests-view-run='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_run.py'
alias stests-view-run-deploys='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_run_deploys.py'
alias stests-view-runs='_exec_cmd $STESTS_PATH_SH_SCRIPTS/view_runs.py'

# ###############################################################
# ALIASES: Direct deploys
# ###############################################################

alias stests-dispatch-transfers-native='_exec_cmd $STESTS_PATH_SH_SCRIPTS/dispatch_transfers_native.py'
alias stests-dispatch-transfers-wasm='_exec_cmd $STESTS_PATH_SH_SCRIPTS/dispatch_transfers_wasm.py'

# ###############################################################
# ALIASES: Generators
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

# WG-1xx: Token transfers:
alias stests-wg-100='_exec_generator 100'       # wasm-less
alias stests-wg-101='_exec_generator 101'       # wasm-less (fire & forget)
alias stests-wg-110='_exec_generator 110'       # wasm per deploy
alias stests-wg-111='_exec_generator 111'       # wasm per deploy (fire & forget)

# WG-2xx: Auction:
alias stests-wg-200='_exec_generator 200'       # validator slot bid submit
alias stests-wg-201='_exec_generator 201'       # validator slot bid withdraw
alias stests-wg-210='_exec_generator 210'       # delegation submit
alias stests-wg-211='_exec_generator 211'       # delegation withdraw
