import typing

from stests.core.clx import utils
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger



def stream_events(
    src: typing.Union[NodeIdentifier, NetworkIdentifier],
    on_block_added: typing.Callable = None,
    on_block_finalized: typing.Callable = None,
    on_deploy_added: typing.Callable = None,
    on_deploy_discarded: typing.Callable = None,
    on_deploy_finalized: typing.Callable = None,
    on_deploy_orphaned: typing.Callable = None,
    on_deploy_processed: typing.Callable = None,
    on_deploy_requeued: typing.Callable = None,
    ):
    """Hooks upto network streaming events.

    :param src: The source from which a network node will be derived.
    :param on_block_added: Callback to invoke whenever a block is added to chain.
    :param on_block_finalized: Callback to invoke whenever a block is finalized.

    """
    for node, event in _yield_events(src):
        event_id = event.event_id

        if on_block_added and event.HasField("block_added"):
            block_hash = event.block_added.block.summary.block_hash.hex()
            on_block_added(node, event_id, block_hash)

        elif on_block_finalized and event.HasField("new_finalized_block"):
            block_hash = event.new_finalized_block.block_hash.hex()
            on_block_finalized(node, event_id, block_hash)

        elif on_deploy_added and event.HasField("deploy_added"):
            deploy_hash = event.deploy_added.deploy.deploy_hash.hex()
            on_deploy_added(node, event_id, deploy_hash)

        elif on_deploy_discarded and event.HasField("deploy_discarded"):
            deploy_hash = event.deploy_discarded.deploy.deploy_hash.hex()
            on_deploy_discarded(node, event_id, deploy_hash)

        elif on_deploy_finalized and event.HasField("deploy_finalized"):
            block_hash = event.deploy_finalized.block_hash.hex()
            deploy_hash = event.deploy_finalized.processed_deploy.deploy.deploy_hash.hex()
            on_deploy_finalized(node, event_id, block_hash, deploy_hash)

        elif on_deploy_orphaned and event.HasField("deploy_orphaned"):
            deploy_hash = event.deploy_orphaned.deploy.deploy_hash.hex()
            on_deploy_orphaned(node, event_id, deploy_hash)

        elif on_deploy_processed and event.HasField("deploy_processed"):
            block_hash = event.deploy_processed.block_hash.hex()
            deploy_hash = event.deploy_processed.processed_deploy.deploy.deploy_hash.hex()
            on_deploy_processed(node, event_id, block_hash, deploy_hash)

        elif on_deploy_requeued and event.HasField("deploy_requeued"):
            deploy_hash = event.deploy_requeued.deploy.deploy_hash.hex()
            on_deploy_requeued(node, event_id, deploy_hash)

        else:
            logger.log_warning(f"CHAIN :: events :: event skipped as type is unsupported :: node={node.address} :: event-id={event_id}")
            print(event)
            pass


def _yield_events(src: typing.Union[NodeIdentifier, NetworkIdentifier]):
    """Yields events from event source (i.e. a CLX chain).
    
    """
    node, client = utils.get_client(src)
    logger.log(f"CHAIN :: events :: binding to stream :: node={node.address}")
    for event in client.stream_events(all=True):
        yield node, event
