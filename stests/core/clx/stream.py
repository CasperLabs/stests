import typing

from stests.core import factory
from stests.core.clx import pyclx
from stests.core.types.infra import NodeEventType
from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger


def stream_events(node_id: NodeIdentifier, event_callback: typing.Callable):
    """Hooks upto network streaming events.

    :param src: The source from which a node client will be instantiated.
    :param event_callback: Callback to invoke whenever an event of relevant type is recieved.

    """
    node, client = pyclx.get_client(node_id)
    logger.log(f"CHAIN :: events :: binding to stream :: node={node.address}")
    for info in client.stream_events(all=True):
        # Set fields according to event type.
        if info.HasField("block_added"):
            event_type=NodeEventType.BLOCK_ADD
            block_hash=info.block_added.block.summary.block_hash.hex()
            deploy_hash=None

        elif info.HasField("new_finalized_block"):
            event_type=NodeEventType.BLOCK_FINALIZED
            block_hash=info.new_finalized_block.block_hash.hex()
            deploy_hash=None

        elif info.HasField("deploy_added"):
            event_type=NodeEventType.DEPLOY_ADDED
            block_hash=None
            deploy_hash=info.deploy_added.deploy.deploy_hash.hex()

        elif info.HasField("deploy_discarded"):
            event_type=NodeEventType.DEPLOY_DISCARDED
            block_hash=None
            deploy_hash=info.deploy_discarded.deploy.deploy_hash.hex()

        elif info.HasField("deploy_finalized"):
            event_type=NodeEventType.DEPLOY_FINALIZED
            block_hash=info.deploy_finalized.block_hash.hex()
            deploy_hash=info.deploy_finalized.processed_deploy.deploy.deploy_hash.hex()

        elif info.HasField("deploy_orphaned"):
            event_type=NodeEventType.DEPLOY_ORPHANED
            block_hash=None
            deploy_hash=info.deploy_orphaned.deploy.deploy_hash.hex()

        elif info.HasField("deploy_processed"):
            event_type=NodeEventType.DEPLOY_PROCESSED
            block_hash=info.deploy_processed.block_hash.hex()
            deploy_hash=info.deploy_processed.processed_deploy.deploy.deploy_hash.hex()

        elif info.HasField("deploy_requeued"):
            event_type=NodeEventType.DEPLOY_REQUEUED
            block_hash=None
            deploy_hash=info.deploy_requeued.deploy.deploy_hash.hex()

        else:
            logger.log_warning(f"CHAIN :: events :: event skipped as type is unsupported :: node={node.address} :: event-id={info.event_id}")
            continue

        # Invoke callback.
        event_callback(node, factory.create_node_event_info(
                node=node, 
                event_id=info.event_id, 
                event_type=event_type,
                block_hash=block_hash,
                deploy_hash=deploy_hash,
            ))
