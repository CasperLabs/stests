import dramatiq
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.middleware import Shutdown

from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import NodeEventType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.infra import NodeMonitoringLock
from stests.monitoring.events import listener



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.control"

# Number of monitors to launch per node.
# TODO: use algo: processes * threads / nodes 
_MONITORS_PER_NODE = 1

# Time limit for node monitoring actor.
_24_HOURS_IN_MS = 86400000


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


@dramatiq.actor(queue_name=_QUEUE, notify_shutdown=True, time_limit=_24_HOURS_IN_MS)
def do_monitor_node(node_id: NodeIdentifier):   
    """Launches node monitoring.
    
    :node_id: Identifier of node to be monitored.

    """
    # Attempt to obtain a lock.
    locked = False
    for i in range(_MONITORS_PER_NODE):
        lock = factory.create_node_monitoring_lock(node_id, i + 1)
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
        log_event(NodeEventType.API_ERROR, node_id, err)
        do_monitor_node.send(node_id)

    # Release lock.
    finally:
        cache.monitoring.delete_node_monitor_lock(lock)
