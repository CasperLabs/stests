import dramatiq

from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.events.deploy.requeued"


@dramatiq.actor(queue_name=_QUEUE)
def on_deploy_requeued(node_id: NodeIdentifier, deploy_hash: str):   
    """Event: raised whenever a deploy is requeued.

    :param node_id: Identifier of node from which event was streamed.
    :param deploy_hash: Hash of requeued deploy.

    """
    logger.log(f"MONIT :: {node_id.label} -> deploy requeued :: {deploy_hash}")
