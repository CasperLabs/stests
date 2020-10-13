import random
import time

import dramatiq
from dramatiq.middleware import TimeLimitExceeded
from dramatiq.middleware import Shutdown

from stests.core import cache
from stests.core import factory
from stests.core.logging import log_event
from stests.core.types.infra import NodeIdentifier
from stests.core.types.infra import NodeMonitoringLock
from stests.core.utils.env import get_var
from stests.monitoring import listener
from stests.events import EventType



# Queue to which messages will be dispatched.
_QUEUE = "monitoring.control"

# Number of monitors to launch per process.
_MONITORS_PER_PROCESS = 8

# Number of monitors to launch per node.
_MONITORS_PER_NODE = 1

# Time limit for node monitoring actor.
_30_MINUTES_IN_MS = 1800000


@dramatiq.actor(queue_name=_QUEUE)
def do_start_monitoring():
    """Starts monitoring of registered networks.
    
    """
    # TODO: reduce number of instantiated monitors.
    for network in cache.infra.get_networks():
        network_id = factory.create_network_id(network.name)
        nodeset = cache.infra.get_nodes_for_monitoring(network_id, 3)
        for node in nodeset:
            if node != nodeset[0]:
                time.sleep(float(1))
            do_monitor_node.send(
                factory.create_node_id(network_id, node.index)
                )


@dramatiq.actor(queue_name=_QUEUE, notify_shutdown=True, time_limit=_30_MINUTES_IN_MS)
def do_monitor_node(node_id: NodeIdentifier):   
    """Launches node monitoring.
    
    :node_id: Identifier of node to be monitored.

    """
    # Attempt to obtain a lock.
    locked = False
    for i in range(_MONITORS_PER_NODE):
        lock = factory.create_node_monitoring_lock(node_id, i + 1)
        _, lock_acquired = cache.monitoring_locks.set_node_monitor_lock(lock)
        if lock_acquired:
            break

    # Escape if sufficient locks are already in place.
    if not lock_acquired:
        return

    # Monitor node by listening to & processing node events.
    try:
        listener.bind_to_stream(
            cache.infra.get_node_by_identifier(node_id)
            )

    # Exception: actor timeout.
    except TimeLimitExceeded:
        do_monitor_node.send(node_id)

    # Exception: process shutdown.
    except Shutdown:
        pass

    # Exception: chain exception, e.g. node down, comms channel issue ...etc.
    except Exception as err:
        log_event(EventType.MONIT_STREAM_BIND_ERROR, err, node_id)
        do_monitor_node.send(node_id)

    # Release lock.
    finally:
        cache.monitoring_locks.delete_node_monitor_lock(lock)
