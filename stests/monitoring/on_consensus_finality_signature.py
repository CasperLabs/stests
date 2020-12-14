from datetime import datetime
import typing

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.consensus.fault"


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
    def deploy_hashes(self):
        """Gets set of associated deploy hashes."""
        try:
            return self.on_chain_block['header']['deploy_hashes']
        except KeyError:
            return []            

    @property
    def deploy_execution_ctx(self):
        """Returns workload generated execution context."""
        return cache.orchestration.get_context(
            self.deploy.network,
            self.deploy.run_index,
            self.deploy.run_type,
            )


@dramatiq.actor(queue_name=_QUEUE)
def on_consensus_finality_signature(info: NodeEventInfo):   
    """Event: raised whenever a consensus finality signature is emitted by a node.

    :param info: Node event information.

    """
    if _is_block_processed(info):
        return

    ctx = _Context(info)
    _process_block(ctx)
    # for deploy_hash in ctx.deploy_hashes:
    #     ctx.deploy_hash = deploy_hash
    #     if not _is_deploy_processed(ctx):
    #         _process_deploy(ctx)




def _is_block_processed(info: NodeEventInfo) -> bool:
    """Returns flag indicating whether finalised deploy event has already been processed.

    """
    # Attempt to cache.
    _, encached = cache.monitoring.set_block(info)

    # Return flag indicating whether block has effectively already been processed.
    return not encached


def _process_block(ctx: _Context):
    """Processes a finalised block.
    
    """
    # Escape if block not found.
    try:
        ctx.on_chain_block = chain.get_block(ctx.network, ctx.node, ctx.block_hash)
    except Exception as err:
        log_event(EventType.CHAIN_QUERY_BLOCK_NOT_FOUND, None, ctx.block_hash)
        return

    # Escape if block empty.
    if not ctx.deploy_hashes:
        log_event(EventType.CHAIN_ADDED_BLOCK_EMPTY, None, ctx.block_hash)
        return
    
    # Set stats.
    ctx.block = factory.create_block_statistics_on_addition(
        block_hash = ctx.block_hash,
        block_hash_parent = ctx.on_chain_block['header']['parent_hash'],
        chain_name = ctx.network.chain_name,
        consensus_era_id = ctx.on_chain_block['header']['era_id'],
        deploy_cost_total = None,
        deploy_count = len(ctx.deploy_hashes),
        deploy_gas_price_avg = None,
        height = ctx.on_chain_block['header']['height'],
        is_switch_block = ctx.on_chain_block['header']['era_end'] is not None,
        network = ctx.network.name,
        proposer = ctx.on_chain_block['header']['proposer'],      
        size_bytes = None,
        state_root_hash = ctx.on_chain_block['header']['state_root_hash'],
        status = BlockStatus.FINALIZED.name,
        timestamp = datetime.strptime(ctx.on_chain_block['header']['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ"),
    )

    # Emit event.
    log_event(EventType.CHAIN_ADDED_BLOCK, f"{ctx.block_hash}", ctx.block)
