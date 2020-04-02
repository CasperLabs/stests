import dramatiq

from stests.core.domain import NodeIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.discarded"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_discarded(node_id: NodeIdentifier, deploy_hash: str):   
    """Event: raised whenever a deploy is discarded.

    :param node_id: Identifier of node from which event was streamed.
    :param deploy_hash: Hash of discarded deploy.

    """
    logger.log(f"MONIT :: {node_id.label} -> deploy discarded :: {deploy_hash}")
