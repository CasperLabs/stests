import dramatiq

from stests.core.domain import NodeIdentifier
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
    logger.log(f"MTRNG :: {node_id.label} -> deploy finalized :: {deploy_hash} :: block-hash={block_hash}")
