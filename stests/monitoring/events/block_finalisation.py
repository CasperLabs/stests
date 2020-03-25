from datetime import datetime

import dramatiq
from google.protobuf.json_format import MessageToDict

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import Block
from stests.core.domain import BlockLock
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger
from stests.orchestration.actors import on_step_deploy_finalized


# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_block(node_id: NodeIdentifier, block_hash: str):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which block was streamed.
    :param block_hash: Hash of finalized block.

    """
    # Query chain.
    block_info = clx.get_block_by_node(node_id, block_hash)

    # Set block summary.
    block = factory.create_block(
        network_id=node_id.network,
        block_hash=block_hash,
        deploy_cost_total=block_info.status.stats.deploy_cost_total,
        deploy_count=block_info.summary.header.deploy_count, 
        deploy_gas_price_avg=block_info.status.stats.deploy_gas_price_avg,
        j_rank=block_info.summary.header.j_rank,
        m_rank=block_info.summary.header.main_rank,
        size_bytes=block_info.status.stats.block_size_bytes,
        timestamp=datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
        validator_id=block_info.summary.header.validator_public_key.hex()
        )
    block.update_on_finalization()

    # Encache block summary (escape if duplicate).    
    _, encached = cache.monitoring.set_block(block)
    if encached:
        logger.log(f"PYCLX :: processing finalized block: bhash={block_hash}")

        # Encache block info.    
        cache.monitoring.set_block_info(block, MessageToDict(block_info))
    
        # Query chain & process deploys. 
        for deploy_hash, deploy_info in clx.get_deploys_by_node(node_id, block_hash):
            _process_finalized_deploy(node_id.network, block, deploy_hash, deploy_info)


def _process_finalized_deploy(network_id: NetworkIdentifier, block: Block, deploy_hash: str, deploy_info: dict):
    """Performs finalized deploy processing.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param block: Finalized block summary.
    :param deploy_hash: Hash of finalized deploy.
    :param deploy_info: Deploy information returned from node.

    """
    logger.log(f"PYCLX :: processing finalized deploy: bhash={block.hash} :: dhash={deploy_hash}")

    # Set deploy summary.
    deploy = factory.create_deploy(network_id, block, deploy_hash, DeployStatus.FINALIZED)

    # Encache deploy summary + info.
    cache.monitoring.set_deploy(block, deploy)
    cache.monitoring.set_deploy_info(block, deploy, deploy_info)

    # Process run deploy - escape if N/A.
    run_deploy = cache.state.get_deploy(deploy_hash)
    if run_deploy:
        _process_finalized_deploy_for_run(block, run_deploy)


def _process_finalized_deploy_for_run(block: Block, deploy: Deploy):
    """Performs finalized deploy processing.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param block: Finalized block summary.
    :param deploy: A deploy that had been dispatched.

    """
    logger.log(f"PYCLX :: run deploy finalized: dhash={deploy.hash} :: bhash={block.hash}")

    # Update deploy.
    deploy.update_on_finalization(block)
    cache.state.set_deploy(deploy)

    # Increment deploy counts.
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)
    cache.orchestration.increment_deploy_counts(ctx)

    # Update transfers.
    transfer = cache.state.get_transfer(deploy.hash)
    if transfer:
        transfer.update_on_completion()
        cache.state.set_transfer(transfer)
    
    # Signal to orchestrator.
    on_step_deploy_finalized.send(ctx, block.hash, deploy.hash)
