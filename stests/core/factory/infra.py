from datetime import datetime

from stests.core.types.infra import Network
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NetworkStatus
from stests.core.types.infra import NetworkType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeMonitoringLock
from stests.core.types.infra import NodeStatus
from stests.core.types.infra import NodeType
from stests.events import EventType



def create_network(name_raw: str, chain_name: str) -> Network:
    """Returns a domain object instance: Network.

    """
    identifier = create_network_id(name_raw)

    return Network(
        chain_name=chain_name,
        faucet=None,
        index=identifier.index,
        name=identifier.name,
        name_raw=name_raw,
        status=NetworkStatus.HEALTHY,
        typeof=identifier.type
    )


def create_network_id(name_raw: str) -> NetworkIdentifier:
    """Returns a cache identifier: NetworkIdentifier.

    """
    # If name has already been parsed.
    if name_raw.upper() == name_raw:
        return NetworkIdentifier(name_raw)

    # Parse raw name.
    name_raw = name_raw.lower()
    for network_type in NetworkType:
        network_type_name = network_type.name.lower()
        if name_raw.startswith(network_type_name):
            index = int(name_raw[len(network_type_name):])
            typeof = name_raw[:len(network_type_name)].upper()
            name = f"{typeof}-{str(index).zfill(2)}"
            return NetworkIdentifier(name=name)

    raise ValueError("Network identifier is unsupported")


def create_node(
    host: str,
    index: int,
    network_id: NetworkIdentifier,
    port_rest: int,
    port_rpc: int,
    port_event: int,
    typeof: NodeType,
    status=NodeStatus.HEALTHY,
    weight=0,
    ) -> Node:
    """Returns a domain object instance: Node.

    """
    return Node(
        account=None,
        host=host,
        index=index,
        network=network_id.name,
        port_rest=port_rest,
        port_rpc=port_rpc,
        port_event=port_event,
        status=status,
        typeof=typeof,
        weight=weight,
    )


def create_node_id(network_id: NetworkIdentifier, index: int) -> NodeIdentifier:
    """Returns a cache identifier: NodeIdentifier.

    """
    return NodeIdentifier(network_id, index)


def create_node_monitoring_lock(node_id: NodeIdentifier, lock_index: int) -> NodeMonitoringLock:
    """Returns a domain object instance: NodeMonitoringLock.

    """
    return NodeMonitoringLock(
        network=node_id.network.name,
        index=node_id.index,
        lock_index=lock_index,
        )


def create_node_event_info(
    node: Node,
    event_id: int,
    event_type: EventType,
    block_hash: str = None,
    deploy_hash: str = None,
    ) -> NodeEventInfo:
    """Returns a domain object instance: NodeEventInfo.

    """
    return NodeEventInfo(
        block_hash=block_hash,
        deploy_hash=deploy_hash,
        event_id=event_id,
        event_timestamp=datetime.now(),
        event_type=event_type,
        network=node.network,
        node_address=node.address_event,
        node_index=node.index,
        )
