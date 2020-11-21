from datetime import datetime
import typing

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.chain import BlockStatus
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventInfo
from stests.events import EventType

from stests.core.types.chain import Deploy
from stests.core.types.infra import NodeIdentifier


# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(info: NodeEventInfo):   
    """Event: raised whenever a block is finalized.

    :param info: Node event information.

    """
    # Escape if already processed.
    # if _is_block_processed(info):
    #     return

    # Set network / node.
    network_id = factory.create_network_id(info.network)
    network = cache.infra.get_network(network_id)
    node_id = factory.create_node_id(network_id, info.node_index)
    node = cache.infra.get_node(node_id)

    # Process block.
    _process_block(info, network, node)


def _is_block_processed(info: NodeEventInfo) -> bool:
    """Returns flag indicating whether finalised block has already been processed.

    """
    # Set summary information.
    summary = factory.create_block_summary(info, BlockStatus.FINALIZED)
    
    # Attempt to cache.
    _, encached = cache.monitoring.set_block_summary(summary)

    # Return flag indicating whether the block has eefectively already been processed.
    return not encached


def _is_deploy_processed(info: NodeEventInfo, deploy_hash: str) -> bool:
    """Returns flag indicating whether finalised deploy event has already been processed.

    """
    summary = factory.create_deploy_summary(info, DeployStatus.FINALIZED)
    
    _, encached = cache.monitoring.set_deploy_summary(summary)

    return not encached


def _process_block(info: NodeEventInfo, network: Network, node: Node):
    """Processes a finalised block.
    
    """
    # Set block - escape if not found.
    try:
        block = chain.get_block(network, node, info.block_hash)
    except Exception as err:
        log_event(EventType.CHAIN_QUERY_BLOCK_NOT_FOUND, None, info.block_hash)
        return

    # Set deploy hashes - escape if not found.
    # if not block['header']['deploy_hashes']:
    #     log_event(EventType.CHAIN_FINALIZED_BLOCK_EMPTY, None, info.block_hash)
    #     return
    
    # Set stats.
    block_stats = factory.create_block_statistics_on_finalization(
        block_hash = block['hash'],
        block_hash_parent = block['header']['parent_hash'],
        chain_name = network.chain_name,
        deploy_cost_total = None,
        deploy_count = len(block['header']['deploy_hashes']),
        deploy_gas_price_avg = None,
        era_id = block['header']['era_id'],
        height = block['header']['height'],
        is_switch_block = block['header']['era_end'] is not None,
        network = network.name,
        size_bytes = None,
        state_root_hash = block['header']['state_root_hash'],
        status = BlockStatus.FINALIZED.name,
        timestamp = datetime.fromtimestamp(block['header']['timestamp']),
        proposer_account_key = block['header']['proposer'],      
    )

    # Emit event: CHAIN_FINALIZED_BLOCK.
    log_event(EventType.CHAIN_FINALIZED_BLOCK, f"{info.block_hash}", block_stats)

    # Process deploys.
    # for deploy_hash in block['header']['deploy_hashes']:
    #     _process_deploy(info, network, node, deploy_hash)


def _process_deploy(info: NodeEventInfo, network: Network, node: Node, deploy_hash: str):
    """Processes a finalised deploy.
    
    """    
    # Escape if already processed.
    if _is_deploy_processed(info, deploy_hash):
        return    

    # Set deploy - escape if not found.
    try:
        deploy = chain.get_deploy(network, node, deploy_hash)
    except Exception as err:
        log_event(EventType.CHAIN_QUERY_DEPLOY_NOT_FOUND, None, deploy_hash)
        return


    # Emit event.
    log_event(EventType.CHAIN_FINALIZED_DEPLOY, f"{info.block_hash}.{info.deploy_hash}", info)

    # Escape if deploy cannot be correlated to a workflow.
    correlated_deploy = cache.state.get_deploy_on_finalisation(info.network_name, info.deploy_hash)
    if not correlated_deploy:
        return

    # Process correlated - i.e. deploys previously dispatched by a generator.
    _process_correlated(
        node_id,
        info,
        datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
        correlated_deploy,
        deploy_info['processingResults'][0].get('cost', 0),
        block_info.summary.header.round_id
        )


    # TODO: raise deploy finialized event
    # TODO: correlate deploy
    pass


def _process_correlated(
    node_id: NodeIdentifier,
    info: NodeEventInfo,
    block_timestamp: datetime,
    deploy: Deploy,
    deploy_cost: int,
    round_id: int
    ):
    """Process a monitored deploy that was previously dispatched during a generator run.
    
    """
    # Notify.
    log_event(EventType.WFLOW_DEPLOY_CORRELATED, f"{info.block_hash}.{info.deploy_hash}", node_id, block_hash=info.block_hash, deploy_hash=info.deploy_hash)

    # Update cache: deploy.
    deploy.block_hash = info.block_hash
    deploy.deploy_cost = deploy_cost
    deploy.finalization_duration = block_timestamp.timestamp() - deploy.dispatch_timestamp.timestamp()    
    deploy.finalization_node = info.node_address
    deploy.finalization_timestamp = block_timestamp
    deploy.round_id = round_id
    deploy.status = DeployStatus.FINALIZED
    cache.state.set_deploy(deploy)

    # Update cache: account balance.
    if deploy_cost > 0:
        cache.state.decrement_account_balance_on_deploy_finalisation(deploy, deploy_cost)

    # Enqueue message for processing by orchestrator.
    _enqueue_correlated(node_id, deploy)


def _enqueue_correlated(node_id: NodeIdentifier, deploy: Deploy):
    """Enqueues a correlated deploy for further processing by orchestrator.
    
    """
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)
    broker = dramatiq.get_broker()
    broker.enqueue(dramatiq.Message(
        queue_name="orchestration.engine.step",
        actor_name="on_step_deploy_finalized",
        args=([
            encoder.encode(ctx),
            encoder.encode(node_id),
            deploy.block_hash,
            deploy.deploy_hash
            ]),
        kwargs=dict(),
        options=dict(),
    ))
