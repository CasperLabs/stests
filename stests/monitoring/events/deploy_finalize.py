from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import encoder
from stests.core import factory
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.core.types.chain import TransferStatus
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_finalized(node_id: NodeIdentifier, event_info: NodeEventInfo):   
    """Event: raised whenever a deploy is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param event_info: Node event information.

    """
    # Unpack event info.
    block_hash = event_info.block_hash
    deploy_hash = event_info.deploy_hash

    # Query chain.
    block_info = clx.get_block_info(node_id, block_hash, parse=False)
    if block_info is None:
        logger.log_error(f"MONIT :: {node_id.label} -> finalized block query failure :: {block_hash}")
        return

    deploy_info = clx.get_deploy_info(node_id, deploy_hash, wait_for_processed=False, parse=True)
    if deploy_info is None:
        logger.log_error(f"MONIT :: {node_id.label} -> finalized deploy query failure :: {deploy_hash}")
        return

    # Process deploys dispatched by a generator.
    deploy = cache.state.get_deploy(deploy_hash)
    if deploy:
        _process_deploy_dispatched_by_a_generator(
            node_id,
            block_hash,
            datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
            deploy,
            deploy_info['processingResults'][0]['cost']
            )


def _process_deploy_dispatched_by_a_generator(
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

    # Update account balance for non-network faucet accounts.
    if not deploy.is_from_network_fauct:
        cache.state.decrement_account_balance_on_deploy_finalisation(deploy)

    # Update transfer.
    transfer = cache.state.get_transfer(deploy.hash)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.state.update_transfer(transfer)

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
