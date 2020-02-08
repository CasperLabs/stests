from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier



def get_key(obj):
    if isinstance(obj, (Network, NetworkIdentifier)):
        return obj.name

    if isinstance(obj, NodeIdentifier):
        key = get_key(obj.network)
        return f"{key}.NODE:{str(obj.node).zfill(4)}"

    if isinstance(obj, Node):
        return f"{obj.network}.NODE:{str(obj.index).zfill(4)}"
