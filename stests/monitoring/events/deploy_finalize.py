from datetime import datetime

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import encoder
from stests.core import factory
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeEventType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.chain import TransferStatus
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.finalized"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_finalized(node_id: NodeIdentifier, info: NodeEventInfo):   
    """Event: raised whenever a deploy is finalized.

    :param node_id: Identifier of node from which event was streamed.
    :param info: Node event information.

    """
    # Query: on-chain block info.
    block_info = clx.get_block_info(node_id, info.block_hash, parse=False)
    if block_info is None:
        logger.log_error(f"CHAIN :: {node_id.label} -> finalized block query failure :: {info.block_hash}")
        return

    # Query: on-chain deploy info.
    deploy_info = clx.get_deploy_info(node_id, info.deploy_hash, wait_for_processed=False, parse=True)
    if deploy_info is None:
        logger.log_error(f"CHAIN :: {node_id.label} -> finalized deploy query failure :: {info.deploy_hash}")
        return

    # Escape if event was already recieved from another node.
    if _was_already_processed(node_id, info):
        return

    # Process deploys dispatched by a generator.
    deploy = cache.state.get_deploy(info.deploy_hash)
    if deploy:
        _process_deploy_dispatched_by_a_generator(
            node_id,
            info,
            datetime.fromtimestamp(block_info.summary.header.timestamp / 1000.0),
            deploy,
            deploy_info['processingResults'][0]['cost']
            )


def _was_already_processed(node_id: NodeIdentifier, info: NodeEventInfo) -> bool:
    """Returns flag indicating whether a finalised deploy has already been processed.

    """
    summary = factory.create_deploy_summary_on_finalisation(node_id, info)
    _, encached = cache.monitoring.set_deploy_summary(summary)

    return not encached


def _process_deploy_dispatched_by_a_generator(
    node_id: NodeIdentifier,
    info: NodeEventInfo,
    block_timestamp: datetime,
    deploy: Deploy,
    deploy_cost: int
    ):
    """Process a monitored deploy that was previously dispatched during a generator run.
    
    """
    logger.log(f"CHAIN :: {node_id.label_index} :: event :: {info.event_id} :: {NodeEventType.DEPLOY_CORRELATED.name} :: {info.deploy_hash}")

    # Update deploy.
    deploy.block_hash = info.block_hash
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
    transfer = cache.state.get_transfer_by_deploy(deploy)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.state.update_transfer(transfer)

    # Signal to workflow orchestrator - note we go down a level in terms of dramtiq usage so as not to import non-monitoring actors.
    ctx = cache.orchestration.get_context(deploy.network, deploy.run_index, deploy.run_type)
    broker = dramatiq.get_broker()
    broker.enqueue(dramatiq.Message(
        queue_name="workflows.orchestration.step",
        actor_name="on_step_deploy_finalized",
        args=([encoder.encode(ctx), encoder.encode(node_id), info.block_hash, deploy.hash]),
        kwargs=dict(),
        options=dict(),
    ))
