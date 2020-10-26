from stests.core import cache
from stests.core import factory



def get_network(args):
    """Maps input args to a target network node.
    
    """
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    return network


def get_network_node(args):
    """Maps input args to a target network node.
    
    """
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    node_id = factory.create_node_id(network_id, int(args.node))
    node = cache.infra.get_node_by_identifier(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    return network, node
