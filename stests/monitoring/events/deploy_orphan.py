import dramatiq

from stests.core.domain import NodeIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.orphaned"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_orphaned(node_id: NodeIdentifier, deploy_hash: str):   
    """Event: raised whenever a deploy is orphaned.

    :param node_id: Identifier of node from which event was streamed.
    :param deploy_hash: Hash of orphaned deploy.

    """
    logger.log(f"MTRNG :: {node_id.label} -> deploy orphaned :: {deploy_hash}")
