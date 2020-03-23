import dramatiq
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.middleware import Shutdown

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.utils import logger
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.domain import NodeStreamLock
from stests.monitoring.events import on_finalized_block



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"

# Number of stream connections to open per network.
# TODO: figure out best way to derive this.
_STREAM_PER_NETWORK_COUNT = 2


@dramatiq.actor(queue_name=_QUEUE)
def do_start_monitoring():
    """Starts monitoring of registered networks.
    
    """
    # Reset all stream locks.
    cache.monitoring.flush_stream_locks()

    # Monitor each network.
    for network in cache.infra.get_networks():
        network_id = factory.create_network_id(network.name)
        do_monitor_network.send(network_id)


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_network(network_id: NetworkIdentifier):
    """Launches network monitoring.
    
    :network_id: Identifier of network to be monitored.

    """
    for node in cache.infra.get_nodes_operational(network_id):
        node_id = factory.create_node_id(network_id, node.index)
        do_monitor_node.send(node_id)


@dramatiq.actor(queue_name=_QUEUE, notify_shutdown=True)
def do_monitor_node(node_id: NodeIdentifier):   
    """Launches node monitoring.
    
    :node_id: Identifier of node to be monitored.

    """
    # Attempt to obtain a stream lock.
    locked = False
    for i in range(_STREAM_PER_NETWORK_COUNT):
        lock = NodeStreamLock(
            network=node_id.network.name,
            node_index=node_id.index,
            lock_index=i + 1
            )
        _, locked = cache.monitoring.set_stream_lock(lock)
        if locked:
            break

    # Escape if sufficient streams are already being processed.
    if not locked:
        return

    # Callback.
    def _on_block_finalized(_, bhash):
        on_finalized_block.send(node_id, bhash)

    # Stream events and re-queue when actor timeout occurs.
    try:
        clx.stream_events(node_id, on_block_finalized=_on_block_finalized)

    # Actor timeout - by default this occurs every 600 seconds.
    except TimeLimitExceeded:
        do_monitor_network.send(node_id.network)

    # Process shutdown.
    except Shutdown:
        pass

    # CLX exception, e.g. node down, comms channel issue ...etc.
    except Exception as err:
        logger.log_warning(f"CHAIN :: stream event error :: {err}")
        do_monitor_network.send(node_id.network)

    # Release lock.
    finally:
        cache.monitoring.delete_stream_lock(lock)
