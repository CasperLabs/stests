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
from stests.core.domain import TransferStatus
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
    # Query chain & set block.
    block_info = clx.get_block_by_node(node_id, block_hash)
    block = factory.create_block_on_finalisation(
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

    # Encache block (escape if duplicate).    
    _, encached = cache.monitoring.set_block(block)
    if not encached:
        return

    # Encache block info.    
    cache.monitoring.set_block_info(block, MessageToDict(block_info))

    # Query chain, process deploys, build collection of run deploys.
    deploys = clx.get_deploys_by_node(node_id, block_hash)
    run_deploys = []
    for deploy_hash, deploy_info in deploys:
        _process_monitored_deploy(node_id, block, deploy_hash, deploy_info)
        run_deploys.append(cache.state.get_deploy(deploy_hash))

    # Process run deploys.
    for idx, run_deploy in enumerate([i for i in run_deploys if i]):
        if idx == 0:
            logger.log(f"PYCLX :: block finalized: block-hash={block.hash}")
        _process_run_deploy(node_id, block, run_deploy)


def _process_monitored_deploy(node_id: NodeIdentifier, block: Block, deploy_hash: str, deploy_info: dict):
    """Performs monitored deploy processing.
    
    """
    # Set deploy summary.
    deploy = factory.create_deploy_on_block_finalisation(node_id, block, deploy_hash)

    # Encache deploy summary + info.
    cache.monitoring.set_deploy(block, deploy)
    cache.monitoring.set_deploy_info(block, deploy, deploy_info)


def _process_run_deploy(node_id: NodeIdentifier, block: Block, deploy: Deploy):
    """Performs a deploy dispatched during a run.
    
    """
    logger.log(f"PYCLX :: deploy finalized: deploy-hash={deploy.hash} :: block-hash={block.hash}")

    # Update deploy.
    deploy.block_hash = block.hash
    deploy.block_rank = block.m_rank
    deploy.status = DeployStatus.FINALIZED
    deploy.finalization_ts = block.timestamp
    deploy.finalization_time = block.timestamp.timestamp() - deploy.dispatch_ts.timestamp()    
    cache.state.set_deploy(deploy)

    # Update transfer.
    transfer = cache.state.get_transfer(deploy.hash)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.state.set_transfer(transfer)

    # Set execution context.
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)

    # Signal to orchestrator.
    on_step_deploy_finalized.send(ctx, node_id, block.hash, deploy.hash)
