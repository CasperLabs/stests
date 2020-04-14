from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import encoder
from stests.core.utils import factory
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import NodeIdentifier
from stests.core.domain import TransferStatus
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_finalized(node_id: NodeIdentifier, block_hash: str, deploy_hash: str):   
    """Event: raised whenever a deploy is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param block_hash: Hash of finalized block.
    :param deploy_hash: Hash of finalized deploy.

    """
    logger.log(f"MONIT :: {node_id.label} -> deploy finalized :: {deploy_hash} :: block={block_hash}")

    # Query chain.
    block_info = clx.get_block_info(node_id, block_hash, parse=False)
    deploy_info = clx.get_deploy_info(node_id, deploy_hash, wait_for_processed=False, parse=True)

    # Set queried fields.
    block_timestamp = datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0)
    deploy_cost = deploy_info['processingResults'][0]['cost']

    # Process a monitored deploy.
    monitored = _set_monitored_deploy(node_id, block_hash, deploy_hash, deploy_cost)

    # Process a dispatched run deploy.
    if monitored:
        deploy = cache.state.get_deploy(deploy_hash)
        if deploy:
            _set_dispatched_deploy(node_id, block_hash, block_timestamp, deploy, deploy_cost)


def _set_monitored_deploy(
    node_id: NodeIdentifier,
    block_hash: str,
    deploy_hash: str,
    deploy_cost: int
    ):
    """Process a monitored deploy.

    :returns: Flag indicating whether deploy had already been monitored.
    
    """
    deploy = factory.create_deploy_on_block_finalisation(
        node_id,
        block_hash,
        deploy_hash,
        deploy_cost
        )
    _, monitored = cache.monitoring.set_deploy(deploy)

    return monitored


def _set_dispatched_deploy(
    node_id: NodeIdentifier,
    block_hash: str,
    block_timestamp: datetime,
    deploy: Deploy,
    deploy_cost: int
    ):
    """Process a monitored deploy that was previously dispatched during a generator run.
    
    """
    logger.log(f"WFLOW :: {deploy.run_type} :: {deploy.label_run_index} :: {deploy.label_phase_index} :: {deploy.label_step_index}  :: {deploy.step_label} :: -> deploy correlated :: {deploy.hash} :: block={block_hash}")

    # Update deploy.
    deploy.block_hash = block_hash
    deploy.cost = deploy_cost
    deploy.status = DeployStatus.FINALIZED
    deploy.finalization_ts = block_timestamp
    deploy.finalization_time = deploy.finalization_ts.timestamp() - deploy.dispatch_ts.timestamp()    
    cache.state.set_deploy(deploy)

    # Update transfer.
    transfer = cache.state.get_transfer(deploy.hash)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.state.set_transfer(transfer)

    # Signal to workflow orchestrator - note we go down a level in terms of dramtiq usage so as not to import non-monitoring actors.
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)
    broker = dramatiq.get_broker()
    broker.enqueue(dramatiq.Message(
        queue_name="workflows.orchestration",
        actor_name="on_step_deploy_finalized",
        args=([encoder.encode(ctx), encoder.encode(node_id), block_hash, deploy.hash]),
        kwargs=dict(),
        options=dict(),
    ))
