import dramatiq
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.middleware import Shutdown

from stests.core import cache
from stests.core.domain import NodeIdentifier
from stests.core.domain import NodeMonitorLock
from stests.core.utils import factory
from stests.core.utils import logger
from stests.monitoring.events import listener



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.control"

# Number of monitors to launch per node.
# TODO: use algo: processes * threads / nodes 
_MONITORS_PER_NODE = 1


@dramatiq.actor(queue_name=_QUEUE)
def do_start_monitoring():
    """Starts monitoring of registered networks.
    
    """
    for network in cache.infra.get_networks():
        network_id = factory.create_network_id(network.name)
        nodeset = cache.infra.get_nodes_operational(network_id)
        for node in nodeset:
            node_id = factory.create_node_id(network_id, node.index)
            do_monitor_node.send(node_id)


@dramatiq.actor(queue_name=_QUEUE, notify_shutdown=True)
def do_monitor_node(node_id: NodeIdentifier):   
    """Launches node monitoring.
    
    :node_id: Identifier of node to be monitored.

    """
    # Attempt to obtain a lock.
    locked = False
    for i in range(_MONITORS_PER_NODE):
        lock = NodeMonitorLock(
            network=node_id.network.name,
            index=node_id.index,
            lock_index=i + 1
            )
        _, lock_acquired = cache.monitoring.set_node_monitor_lock(lock)
        if lock_acquired:
            break

    # Escape if sufficient locks are already in place.
    if not lock_acquired:
        return

    # Monitor node by listening to & processing node events.
    try:
        listener.bind_to_stream(node_id)

    # Exception: actor timeout - by default this occurs every 600 seconds.
    except TimeLimitExceeded:
        do_monitor_node.send(node_id)

    # Exception: process shutdown.
    except Shutdown:
        pass

    # Exception: chain exception, e.g. node down, comms channel issue ...etc.
    except Exception as err:
        logger.log_warning(f"MONIT :: stream :: error :: {err}")
        do_monitor_node.send(node_id)

    # Release lock.
    finally:
        cache.monitoring.delete_node_monitor_lock(lock)
