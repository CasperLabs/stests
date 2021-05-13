import random
import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.infra import Network
from stests.core.types.infra import Node



def get_network(args) -> Network:
    """Maps input args to a target network node.
    
    """
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    return network


def get_network_node(args) -> typing.Tuple[Network, Node]:
    """Maps input args to a target network node.
    
    """
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    node_id = factory.create_node_id(network_id, int(args.node))
    node = cache.infra.get_node(node_id)
    if node is None:
        raise ValueError("Unregistered node.")

    return network, node


def get_network_nodeset(args) -> typing.Tuple[Network, typing.List[Node]]:
    """Maps input args to a target network node.
    
    """
    network_id = factory.create_network_id(args.network)
    network = cache.infra.get_network(network_id)
    if network is None:
        raise ValueError("Unregistered network.")

    nodeset = cache.infra.get_nodes_for_dispatch(network)
    if nodeset is None or len(nodeset) == 0:
        raise ValueError("Unregistered nodeset.")

    return network, sorted(nodeset, key=lambda i: i.index)


def get_network_nodeset_by_node(args) -> typing.Tuple[Network, typing.List[Node]]:
    """Maps input args to a target network nodeset.
    
    """
    network, nodeset = get_network_nodeset(args)    

    # All nodes.
    if args.node == 0:
        return network, nodeset

    # A single node chosen at random.
    if args.node == -1:
        return network, [random.choice(nodeset)]

    # A specific node.
    if isinstance(args.node, int):
        try:
            return network, [nodeset[args.node - 1]]
        except IndexError:
            return network, [random.choice(nodeset)]

    raise ValueError("Invalid node index.")
