from stests.core.domain import Account
from stests.core.domain import AccountStatus
from stests.core.domain import AccountType
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NetworkStatus
from stests.core.domain import NetworkType
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import NodeType
from stests.core.domain import NodeStatus
from stests.core.domain import TypeMetadata



def get_account(
    private_key: str, 
    public_key: str,
    typeof: AccountType,
    status: AccountStatus = AccountStatus.NEW
    ) -> Account:
    """Simple factory that returns an account domain object instance.
    
    :param name_raw: Network name, e.g. lrt1
    :returns: A network instance.

    """
    return Account(
        meta=TypeMetadata(),
        private_key=private_key,
        public_key=public_key,
        status=status or AccountStatus.NEW,
        typeof=typeof
        )


def get_network(name_raw: str) -> Network:
    """Simple factory that returns a network domain object instance.
    
    :param name_raw: Network name, e.g. lrt1
    :returns: A network instance.

    """
    network_id = get_network_identifier(name_raw)

    return Network(
        faucet=None,
        index=network_id.index,
        meta=TypeMetadata(),
        name=network_id.name,
        name_raw=name_raw,
        status=NetworkStatus.NULL,
        typeof=network_id.typeof
    )


def get_network_identifier(name_raw: str) -> NetworkIdentifier:
    """Simple factory that returns a network identifier domain object instance.
    
    :param name_raw: Network name, e.g. lrt1
    :returns: A network identifier instance.

    """
    name_raw = name_raw.lower()
    index=int(name_raw[3:])
    typeof=name_raw[:3].upper()
    name = f"{typeof}-{str(index).zfill(2)}"

    return NetworkIdentifier(name)


def get_node(host: str, index: int, network_id: NetworkIdentifier, port: int, typeof: NodeType) -> Node:
    """Simple factory that returns a node domain object instance.
    
    :param name: Network name, e.g. lrt1
    :returns: A network instance.

    """
    return Node(
        account=None,
        host=host,
        index=index,
        meta=TypeMetadata(),
        network=network_id.name,
        port=port,
        typeof=typeof,
        status=NodeStatus.NULL
    )


def get_node_identifier(network_id: NetworkIdentifier, index: int) -> NodeIdentifier:
    """Simple factory that returns a network identifier domain object instance.
    
    :param name: Network name, e.g. lrt1
    :returns: A network identifier instance.

    """
    return NodeIdentifier(network_id, index)
