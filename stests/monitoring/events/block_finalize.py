from datetime import datetime

import dramatiq
from google.protobuf.json_format import MessageToDict

from stests.core import cache
from stests.core import clx
from stests.core.utils import encoder 
from stests.core.utils import factory
from stests.core.domain import Block
from stests.core.domain import BlockLock
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.domain import TransferStatus
from stests.core.utils import logger


# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.block.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_block_finalized(node_id: NodeIdentifier, block_hash: str):   
    """Event: raised whenever a block is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param block_hash: Hash of finalized block.

    """
    logger.log(f"MONIT :: {node_id.label} -> block finalized :: {block_hash}")

    # Get block info.
    block_info = clx.get_block_by_node(node_id, block_hash)

    # Set block summary.
    block = factory.create_block_on_finalisation(
        node_id=node_id,
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

    # Get deploys & process.
    for deploy_hash, deploy_info in clx.get_deploys_by_node_and_block(node_id, block_hash):

        try:
            deploy_cost = deploy_info['cost']
        except:
            deploy_cost = 0

        _process_deploy(node_id, block, deploy_hash, deploy_cost)
        _process_deploy_of_run(node_id, block, deploy_hash, deploy_cost)


def _process_deploy(node_id: NodeIdentifier, block: Block, deploy_hash: str, deploy_cost: int):
    """Performs monitored deploy processing.
    
    """
    deploy = factory.create_deploy_on_block_finalisation(node_id, block, deploy_hash, deploy_cost)
    cache.monitoring.set_deploy(block, deploy)


def _process_deploy_of_run(node_id: NodeIdentifier, block: Block, deploy_hash: str, deploy_cost: int):
    """Performs a deploy dispatched during a run.
    
    """
    # Set deploy - previously dispatched by a generator.
    deploy = cache.state.get_deploy(deploy_hash)
    if not deploy:
        return
    
    logger.log(f"WFLOW :: {deploy.run_type} :: {deploy.label_run_index} :: {deploy.label_phase_index} :: {deploy.label_step_index}  :: {deploy.step_label} :: -> deploy correlated :: {deploy.hash} :: block={block.hash}")

    # Update deploy.
    deploy.block_hash = block.hash
    deploy.block_rank = block.m_rank
    deploy.cost = deploy_cost
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

    # Signal to workflow orchestrator - note we go down a level in terms of dramtiq usage so as not to import non-monitoring actors.
    broker = dramatiq.get_broker()
    broker.enqueue(dramatiq.Message(
        queue_name="workflows.orchestration",
        actor_name="on_step_deploy_finalized",
        args=([encoder.encode(ctx), encoder.encode(node_id), block.hash, deploy.hash]),
        kwargs=dict(),
        options=dict(),
    ))
