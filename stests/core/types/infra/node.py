import dataclasses
import typing
from datetime import datetime

import pycspr

from stests.core.types.chain.account import Account
from stests.core.types.infra.enums import NodeStatus
from stests.core.types.infra.enums import NodeGroup
from stests.core.types.infra.enums import NodeType
from stests.core.types.infra.network import NetworkIdentifier
from stests.events import EventType



@dataclasses.dataclass
class Node:
    """Encapsulates information pertaining to a node within a target network.

    """
    # Bonding account associated with node.
    account: typing.Optional[Account]

    # Node grouping within network.
    group: typing.Optional[NodeGroup]

    # Node's host address.
    host: str

    # Numerical index to distinguish between nodes, e.g. node-01, node-02 ...etc.
    index: int

    # Network with which node is associated.
    network: str

    # Node's external facing event stream port.
    port_event: int

    # Node's external facing RPC port.
    port_rest: int

    # Node's external facing RPC port.
    port_rpc: int

    # Current node status.
    status: NodeStatus

    # Type of node in terms of it's degree of consensus participation.
    typeof: NodeType

    # Flag indicating whether this node is to be used for dispatch purposes.
    use_to_dispatch: bool

    # Flag indicating whether this node is to be used for monitoring purposes.
    use_to_monitor: bool

    # Flag indicating whether this node is to be used for querying purposes.
    use_to_query: bool

    # POS weight.
    weight: typing.Optional[int]

    @property
    def address(self):
        return f"{self.host}:{self.port_rpc}"

    @property
    def address_event(self):
        return f"{self.host}:{self.port_event}"

    @property
    def address_rest(self):
        return f"{self.host}:{self.port_rest}"

    @property
    def address_rpc(self):
        return f"{self.host}:{self.port_rpc}"

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def is_dispatchable(self):
        return self.use_to_dispatch and \
               self.status in (NodeStatus.HEALTHY, NodeStatus.DISTRESSED)

    @property
    def is_monitorable(self):
        return self.use_to_monitor and \
               self.status == NodeStatus.HEALTHY

    @property
    def is_queryable(self):
        return self.use_to_query and \
               self.status in (NodeStatus.HEALTHY, NodeStatus.DISTRESSED)

    @property
    def label(self):
        return f"{self.network}:NODE-{self.index}"

    @property
    def network_name(self):
        return self.network

    @property
    def url_event(self):
        return f"http://{self.address_event}/events"

    @property
    def url_rest(self):
        return f"http://{self.address_rest}"

    @property
    def url_rpc(self):
        return f"http://{self.address_rpc}/rpc"

    @property
    def identifier(self) -> 'NodeIdentifier':
        network_identifier = NetworkIdentifier(name=self.network_name)

        return NodeIdentifier(
            network=network_identifier,
            index=self.index,
        )
    
    @property
    def client(self) -> pycspr.NodeClient:
        return pycspr.NodeClient(
            pycspr.NodeConnection(
                host=self.host,
                port_rest=self.port_rest,
                port_rpc=self.port_rpc,
                port_sse=self.port_event,
            )
        )

    def dispatch_deploy(self, deploy: pycspr.types.Deploy) -> str:
        """Dispatches a deploy to a node for processing.

        :param deploy: A deploy to be processed at a node.

        """
        return self.client.send_deploy(deploy)


    def get_account(self, account_key: str, block_id: typing.Union[None, bytes, str, int] = None) -> dict:
        """Returns on-chain account information at a certain block.

        :param account_key: An account holder's public key prefixed with a key type identifier.
        :param block_id: Identifier of a finalised block.
        :returns: Account information in JSON format.

        """ 
        return self.client.get_account_info(account_key, block_id)


    def get_account_balance(self, purse_uref: str, state_root_hash: str = None) -> int:    
        """Queries account balance at a certain block height | hash.

        :param purse_uref: URef of a purse associated with an on-chain account.
        :param state_root_hash: A node's root state hash at some point in chain time.
        :returns: Account balance.

        """
        return self.client.get_account_balance(purse_uref, state_root_hash)


    def get_account_main_purse_uref(self, account_key: str, state_root_hash: str = None) -> str:
        """Returns main purse uref for an account.

        :param account_key: Hexadecimal representation of key related to account being pulled.
        :param state_root_hash: State root hash at a node within target network.

        :returns: Account main purse uref.

        """
        uref: pycspr.types.CL_URef = self.client.get_account_main_purse_uref(account_key, state_root_hash)

        return uref.to_string()


    def get_auction_info(self) -> dict:
        """Queries chain for current auction contract information.

        :returns: On-chain auction information.

        """
        return self.client.get_auction_info()


    def get_block(self, block_id: typing.Union[None, bytes, str, int] = None) -> str:
        """Queries a node for a block - returns latest block if hash is not provided.

        :param block_id: Identifier of a finalised block.
        :returns: Representation of a block within a node's state.

        """
        return self.client.get_block(block_id)


    def get_deploy(self, deploy_hash: str = None) -> dict:
        """Queries a node for a deploy.

        :param deploy_hash: Hash of deploy being pulled.
        :returns: Representation of a deploy within a node's state.

        """
        return self.client.get_deploy(deploy_hash)


    def get_node_metrics(self) -> list:
        """Queries a node for it's current metrics.

        :returns: Representation of a node's metrics.

        """
        return self.client.get_node_metrics()


    def get_node_peers(self) -> list:
        """Queries a node for it's current peer set.

        :returns: List of a node's peer set.

        """
        return self.client.get_node_peers()


    def get_node_status(self) -> str:
        """Queries a node for it's current status.

        :returns: Representation of a node's status.

        """
        return self.client.get_node_status()


    def get_state_root_hash(self, block_id: typing.Union[None, bytes, str, int] = None) -> str:
        """Queries a node for it's current state root hash.

        :param block_id: Identifier of a finalised block.
        :returns: Global state root hash at a network node.

        """
        state_root_hash: bytes = self.client.get_state_root_hash(block_id)

        return state_root_hash.hex()


@dataclasses.dataclass
class NodeEventInfo:
    """Encapsulates information pertaining to a node event.

    """
    # Key of an account associated with event.
    account_key: typing.Optional[str]

    # Hash of block associated with event.
    block_hash: typing.Optional[str]

    # Hash of deploy associated with event.
    deploy_hash: typing.Optional[str]

    # Node specific event identifier.
    event_id: int

    # Moment in time when event was streamed.
    event_timestamp: datetime

    # Type of event.
    event_type: EventType

    # Associated network.
    network: str

    # Address of node from which deploy was streamed.
    node_address: str

    # Index of Node from which deploy was streamed.
    node_index: int

    @property
    def label_event_id(self):
        return f"E-{str(self.event_id).zfill(9)}"

    @property
    def label_event_type(self):
        return self.event_type.name

    @property
    def label_node_index(self):
        return f"N-{str(self.node_index).zfill(4)}"

    @property
    def log_suffix(self):
        if self.block_hash and self.deploy_hash:
            return f"{self.deploy_hash} :: block={self.block_hash} :: event={self.event_id}"
        elif self.block_hash:
            return f"{self.block_hash} :: event={self.event_id}"
        elif self.deploy_hash:
            return f"{self.deploy_hash} :: event={self.event_id}"

    @property
    def network_name(self):
        return self.network


@dataclasses.dataclass
class NodeIdentifier:
    """Encapsulates information required to disambiguate between nodes.

    """
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    index: int

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def label(self):
        return f"{self.network.name}:{self.label_index}"

    @property
    def network_id(self):
        return self.network

    @property
    def network_name(self):
        return self.network.name


@dataclasses.dataclass
class NodeMonitoringLock:
    """Encapsulates information used to lock monitoring of a node.

    """
    # Numerical index to distinguish between nodes upon the same network.
    index: int

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple locks.
    lock_index: int

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def label_node_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def network_name(self):
        return self.network
