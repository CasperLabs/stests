from datetime import datetime
import json

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.chain import BlockStatistics
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.core.utils import encoder
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.added"


class _Context():
    """Contextual information passed along chain of execution.
    
    """
    def __init__(self, info: NodeEventInfo):
        self.block = None
        self.block_hash = info.block_hash
        self.deploy = None
        self.info = info
        self.network_id = factory.create_network_id(info.network)
        self.network = cache.infra.get_network(self.network_id)
        self.node_id = factory.create_node_id(self.network_id, info.node_index)
        self.node = cache.infra.get_node(self.node_id)
        self.on_chain_block = None
        self.on_chain_deploy = None
    
    @property
    def deploy_execution_ctx(self):
        """Returns workload generated execution context."""
        return cache.orchestration.get_context(
            self.deploy.network,
            self.deploy.run_index,
            self.deploy.run_type,
            )

    @property
    def deploy_hashes(self):
        """Gets set of associated deploy hashes."""
        try:
            return self.on_chain_block['header']['deploy_hashes']
        except (KeyError, TypeError,):
            return [] 


@dramatiq.actor(queue_name=_QUEUE)
def on_block_added(info: NodeEventInfo):   
    """Event: raised whenever a block is added.

    :param info: Node event information.

    """
    # Escape if already processed.
    _, encached = cache.monitoring.set_block(info)
    if not encached:
        return

    ctx = _Context(info)
    _process_block(ctx)
    for deploy_hash in ctx.deploy_hashes:
        print(deploy_hash)
    #     ctx.deploy_hash = deploy_hash
    #     if not _is_deploy_processed(ctx):
    #         _process_deploy(ctx)


def _is_deploy_processed(ctx: _Context) -> bool:
    """Returns flag indicating whether finalised deploy event has already been processed.

    """
    _, encached = cache.monitoring.set_deploy(ctx.network.name, ctx.block_hash, ctx.deploy_hash)

    return not encached


def _process_block(ctx: _Context):
    """Processes a finalised block.
    
    """
    # Escape if block not found.
    try:
        on_chain_block = chain.get_block(ctx.network, ctx.node, ctx.block_hash)
    except Exception as err:
        log_event(EventType.CHAIN_QUERY_BLOCK_NOT_FOUND, None, ctx.block_hash)
        return

    # Escape if block empty.
    if not on_chain_block['header']['deploy_hashes']:
        log_event(EventType.CHAIN_ADDED_BLOCK_EMPTY, None, ctx.block_hash)
        return
    print(on_chain_block['header']['deploy_hashes'])
    
    # Set stats.
    ctx.block = factory.create_block_statistics_on_addition(
        block_hash = ctx.block_hash,
        block_hash_parent = on_chain_block['header']['parent_hash'],
        chain_name = ctx.network.chain_name,
        consensus_era_id = on_chain_block['header']['era_id'],
        deploy_cost_total = None,
        deploy_count = len(on_chain_block['header']['deploy_hashes']),
        deploy_gas_price_avg = None,
        height = on_chain_block['header']['height'],
        is_switch_block = on_chain_block['header']['era_end'] is not None,
        network = ctx.network.name,
        proposer = on_chain_block['header']['proposer'],      
        size_bytes = None,
        state_root_hash = on_chain_block['header']['state_root_hash'],
        status = BlockStatus.FINALIZED.name,
        timestamp = datetime.strptime(on_chain_block['header']['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ"),
    )

    # Emit event.
    log_event(EventType.CHAIN_ADDED_BLOCK, f"{ctx.block_hash}", ctx.block)


def _process_deploy(ctx: _Context):
    """Processes a finalised deploy.
    
    """    

    # Set deploy - escape if not found.
    try:
        ctx.on_chain_deploy = chain.get_deploy(ctx.network, ctx.node, ctx.deploy_hash)
    except Exception as err:
        log_event(EventType.CHAIN_QUERY_DEPLOY_NOT_FOUND, None, ctx.deploy_hash)
        return
    
    # Emit event.
    log_event(EventType.CHAIN_ADDED_DEPLOY, f"{ctx.block_hash}.{ctx.deploy_hash}", ctx.info)

    # Escape if deploy cannot be correlated to a workflow.
    ctx.deploy = cache.state.get_deploy_on_finalisation(ctx.network.name, ctx.deploy_hash)
    if not ctx.deploy:
        return

    # Process correlated - i.e. deploys previously dispatched by a generator.
    _process_deploy_correlated(ctx)


def _process_deploy_correlated(ctx: _Context):
    """Process a monitored deploy that was previously dispatched during a generator run.
    
    """
    # Notify.
    log_event(EventType.WFLOW_DEPLOY_CORRELATED, f"{ctx.block_hash}.{ctx.deploy_hash}", ctx.node, block_hash=ctx.block_hash, deploy_hash=ctx.deploy_hash)

    # Update cache: deploy.
    ctx.deploy.block_hash = ctx.block_hash
    ctx.deploy.deploy_cost = int(ctx.on_chain_deploy["execution_results"][0]["result"]["cost"])
    # deploy.consensus_round_id = ctx.block.consensus_round_id
    ctx.deploy.consensus_era_id = ctx.block.consensus_era_id
    ctx.deploy.finalization_duration = ctx.block.timestamp.timestamp() - ctx.deploy.dispatch_timestamp.timestamp()    
    ctx.deploy.finalization_node_index = ctx.node.index
    ctx.deploy.finalization_timestamp = ctx.block.timestamp
    ctx.deploy.state_root_hash = ctx.block.state_root_hash
    ctx.deploy.status = DeployStatus.ADDED
    cache.state.set_deploy(ctx.deploy)

    # # Update cache: account balance.
    # if deploy_cost > 0:
    #     cache.state.decrement_account_balance_on_deploy_finalisation(ctx.deploy, ctx.deploy.deploy_cost)

    # # Enqueue message for processing by orchestrator.
    _enqueue_correlated(ctx)


def _enqueue_correlated(ctx: _Context):
    """Enqueues a correlated deploy for further processing by orchestrator.
    
    """
    broker = dramatiq.get_broker()
    broker.enqueue(dramatiq.Message(
        queue_name="orchestration.engine.step",
        actor_name="on_step_deploy_finalized",
        args=([
            encoder.encode(ctx.deploy_execution_ctx),
            encoder.encode(ctx.node_id),
            ctx.block_hash,
            ctx.deploy_hash
            ]),
        kwargs=dict(),
        options=dict(),
    ))
