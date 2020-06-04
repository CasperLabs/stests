from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import encoder
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeIdentifier
from stests.core.types.chain import TransferStatus
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_finalized(node_id: NodeIdentifier, info: NodeEventInfo):   
    """Event: raised whenever a deploy is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param info: Node event information.

    """
    # Escape if on-chain info not found.
    block_info = clx.get_block_info(node_id, info.block_hash, parse=False)
    if block_info is None:
        log_event(EventType.MONITORING_BLOCK_NOT_FOUND, None, node_id, block_hash=info.block_hash)
        return

    # Escape if on-chain info not found.
    deploy_info = clx.get_deploy_info(node_id, info.deploy_hash, wait_for_processed=False, parse=True)
    if deploy_info is None:
        log_event(EventType.MONITORING_DEPLOY_NOT_FOUND, None, node_id, block_hash=info.block_hash, deploy_hash=info.deploy_hash)
        return

    # Escape if event already received from another node.
    if _already_processed(info):
        return

    # Process correlated.
    deploy = cache.state.get_deploy_on_finalisation(info.network_name, info.deploy_hash)
    if deploy:
        _process_correlated(
            node_id,
            info,
            datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
            deploy,
            deploy_info['processingResults'][0]['cost'],
            block_info.summary.header.round_id
            )


def _already_processed(info: NodeEventInfo) -> bool:
    """Returns flag indicating whether finalised deploy event has already been processed.

    """
    summary = factory.create_deploy_summary_on_finalisation(info)
    _, encached = cache.monitoring.set_deploy_summary(summary)

    return not encached


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
    log_event(EventType.MONITORING_DEPLOY_CORRELATED, None, node_id, block_hash=info.block_hash, deploy_hash=info.deploy_hash)

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
    cache.state.decrement_account_balance_on_deploy_finalisation(deploy, deploy_cost)

    # Update cache: transfer.
    transfer = cache.state.get_transfer_by_deploy(deploy)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.state.set_transfer(transfer)

    # Emit event.
    log_event(EventType.CHAININFO_FINALIZED_DEPLOY, None, deploy)

    # Enqueue message for processing by orchestrator.
    _enqueue_correlated(node_id, deploy)


def _enqueue_correlated(node_id: NodeIdentifier, deploy: Deploy):
    """Enqueues a correlated deploy for further processing by orchestrator.
    
    """
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)
    broker = dramatiq.get_broker()
    broker.enqueue(dramatiq.Message(
        queue_name="workflows.orchestration.step",
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
