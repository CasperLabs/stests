import dramatiq

from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.added"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_added(node_id: NodeIdentifier, deploy_hash: str):   
    """Event: raised whenever a deploy is added.

    :param node_id: Identifier of node from which event was streamed.
    :param block_hash: Hash of added block.
    :param deploy_hash: Hash of added deploy.

    """
    logger.log(f"MONIT :: {node_id.label} -> deploy added :: {deploy_hash}")
