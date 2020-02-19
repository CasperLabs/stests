from stests.core.cache.utils import encache
from stests.core.domain import Block
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node



@encache
def set_network(network: Network):
    """Encaches domain object: Network.
    
    """
    return [
        "network",
        network.name,
    ], network


@encache
def set_network_block(network_id: NetworkIdentifier, block: Block):
    """Encaches domain object: Block.
    
    """
    return [
        "network-block",
        network_id.name,
        f"{str(block.timestamp)}.{block.bhash}"
    ], block
    

@encache
def set_network_node(node: Node):
    """Encaches domain object: Node.
    
    """
    return [
        "network-node",
        node.network,
        f"N-{str(node.index).zfill(4)}"
    ], node
