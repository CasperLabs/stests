from stests.core import clx
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.utils import logger
from stests.monitoring.events.block_add import on_block_added
from stests.monitoring.events.block_finalize import on_block_finalized
from stests.monitoring.events.deploy_add import on_deploy_added
from stests.monitoring.events.deploy_discard import on_deploy_discarded
from stests.monitoring.events.deploy_finalize import on_deploy_finalized
from stests.monitoring.events.deploy_orphan import on_deploy_orphaned
from stests.monitoring.events.deploy_processed import on_deploy_processed
from stests.monitoring.events.deploy_requeue import on_deploy_requeued



def bind_to_stream(node_id: NodeIdentifier):
    """Binds to a node's event stream.

    :node_id: Identifier of node being monitored.
    
    """

    def _on_block_added(node: Node, event_info, event_id: int, block_hash: str):
        """Callback: on_block_added.
        
        """
        on_block_added.send(node_id, block_hash)


    def _on_block_finalized(node: Node, event_info, event_id: int, block_hash: str):
        """Callback: on_block_finalized.
        
        """
        on_block_finalized.send(node_id, block_hash)


    def _on_deploy_added(node: Node, event_info, event_id: int, deploy_hash: str):
        """Callback: on_deploy_added.
        
        """
        on_deploy_added.send(node_id, deploy_hash)


    def _on_deploy_discarded(node: Node, event_info, event_id: int, deploy_hash: str):
        """Callback: on_deploy_discarded.
        
        """
        on_deploy_discarded.send(node_id, deploy_hash)


    def _on_deploy_finalized(node: Node, event_info, event_id: int, block_hash: str, deploy_hash: str):
        """Callback: on_deploy_finalized.
        
        """
        on_deploy_finalized.send(node_id, block_hash, deploy_hash)


    def _on_deploy_orphaned(node: Node, event_info, event_id: int, deploy_hash: str):
        """Callback: on_deploy_orphaned.
        
        """
        on_deploy_orphaned.send(node_id, deploy_hash)


    def _on_deploy_processed(node: Node, event_info, event_id: int, block_hash: str, deploy_hash: str):
        """Callback: on_deploy_processed.
        
        """
        on_deploy_processed.send(node_id, block_hash, deploy_hash)


    def _on_deploy_requeued(node: Node, event_info, event_id: int, deploy_hash: str):
        """Callback: on_deploy_requeued.
        
        """
        on_deploy_requeued.send(node_id, deploy_hash)


    logger.log(f"MONIT :: node :: start :: {node_id.label}")

    # Bind to a node's stream-events endpoint & dispatch a message to relevant actor.
    clx.stream_events(node_id,
        on_block_added=_on_block_added,
        on_block_finalized=_on_block_finalized,
        on_deploy_added=_on_deploy_added,
        on_deploy_discarded=_on_deploy_discarded,
        on_deploy_finalized=_on_deploy_finalized,
        on_deploy_orphaned=_on_deploy_orphaned,
        on_deploy_processed=_on_deploy_processed,
        on_deploy_requeued=_on_deploy_requeued,
        )
