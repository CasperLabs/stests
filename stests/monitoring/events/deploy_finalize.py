from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import encoder
from stests.core import factory
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import NodeIdentifier
from stests.core.types.chain import TransferStatus
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
    # Escape if event has been processed.
    if _was_event_processed(node_id, block_hash, deploy_hash):
        return

    logger.log(f"MONIT :: {node_id.label} -> deploy finalized :: {deploy_hash} :: block={block_hash}")

    # Query chain.
    block_info = clx.get_block_info(node_id, block_hash, parse=False)
    if block_info is None:
        logger.log_error(f"MONIT :: {node_id.label} -> finalized block query failure :: {block_hash}")
        return

    deploy_info = clx.get_deploy_info(node_id, deploy_hash, wait_for_processed=False, parse=True)
    if deploy_info is None:
        logger.log_error(f"MONIT :: {node_id.label} -> finalized deploy query failure :: {deploy_hash}")
        return

    # TODO: process deploy_info error states
    # import json
    # print(json.dumps(deploy_info, indent=4))

    # Process previously dispatched deploys.
    deploy = cache.state.get_deploy(deploy_hash)
    if deploy:
        _process_dispatched_deploy(
            node_id,
            block_hash,
            datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
            deploy,
            deploy_info['processingResults'][0]['cost']
            )


def _was_event_processed(node_id: NodeIdentifier, block_hash: str, deploy_hash: str) -> bool:
    """Process a monitored deploy & returns a flag indicating whether it was successfully cached.

    """
    summary = factory.create_deploy_summary(
        node_id,
        block_hash,
        deploy_hash,
        )
    _, encached = cache.monitoring.set_deploy_summary(summary)

    return not encached


def _process_dispatched_deploy(
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
    deploy.finalization_node = node_id.index
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
        queue_name="workflows.orchestration.step",
        actor_name="on_step_deploy_finalized",
        args=([encoder.encode(ctx), encoder.encode(node_id), block_hash, deploy.hash]),
        kwargs=dict(),
        options=dict(),
    ))
