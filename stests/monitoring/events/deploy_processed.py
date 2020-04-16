import dramatiq

from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.processed"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_processed(node_id: NodeIdentifier, block_hash: str, deploy_hash: str):   
    """Event: raised whenever a deploy is processed.

    :param node_id: Identifier of node from which event was streamed.
    :param block_hash: Hash of processed block.
    :param deploy_hash: Hash of processed deploy.

    """
    logger.log(f"MONIT :: {node_id.label} -> deploy processed :: {deploy_hash} :: block={block_hash}")
