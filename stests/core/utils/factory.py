import datetime
import typing

from stests.core.cache.identifiers import *
from stests.core.domain import *
from stests.core.utils import crypto
from stests.core.utils.domain import TypeMetadata



def create_account(
    typeof: AccountType,
    index: int = 1,
    private_key: str = None, 
    public_key: str = None,
    status: AccountStatus = AccountStatus.NEW
    ) -> Account:
    """Returns a domain object instance: Account.
    
    """
    if private_key is None:
        private_key, public_key = crypto.generate_key_pair(crypto.KeyEncoding.HEX)        

    return Account(
        index=index or 1,
        private_key=private_key,
        public_key=public_key,
        status=status or AccountStatus.NEW,
        typeof=typeof,
        meta=TypeMetadata()
        )


def create_deploy(hash_id: str, status: DeployStatus) -> Deploy:
    """Returns a domain object instance: Deploy.
    
    """
    return Deploy(
        hash_id=hash_id,
        status=status,
        ts_dispatched=None if status != DeployStatus.DISPATCHED else datetime.datetime.now().timestamp()
    )


def create_network(name_raw: str) -> Network:
    """Returns a domain object instance: Network.
    
    """
    identifier = create_network_id(name_raw)

    return Network(
        faucet=None,
        index=identifier.index,
        name=identifier.name,
        name_raw=name_raw,
        status=NetworkStatus.NULL,
        typeof=identifier.type
    )


def create_network_id(name_raw: str) -> NetworkIdentifier:
    """Returns a domain object instance: NetworkIdentifier.
    
    """
    name_raw = name_raw.lower()
    for network_type in [i.name.lower() for i in NetworkType]:
        if name_raw.startswith(network_type):
            index=int(name_raw[len(network_type):])
            typeof=name_raw[:len(network_type)].upper()
            name = f"{typeof}-{str(index).zfill(2)}"
            return NetworkIdentifier(name=name)

    raise ValueError("Network identifier is unsupported")


def create_node(
    host: str,
    index: int,
    network_id: NetworkIdentifier,
    port: int,
    type: NodeType
    ) -> Node:
    """Returns a domain object instance: Node.
    
    """
    return Node(
        account=None,
        host=host,
        index=index,
        network=network_id.name,
        port=port,
        type=type,
        status=NodeStatus.NULL
    )


def create_node_id(
    network_id: NetworkIdentifier,
    index: int
    ) -> NodeIdentifier:
    """Returns a domain object instance: NodeIdentifier.
    
    """
    return NodeIdentifier(network_id, index)


def create_run_context(
    args: typing.Any,
    index: int,
    network_id: NetworkIdentifier,
    node_id: NodeIdentifier,
    typeof: str
    ) -> RunContext:
    """Returns a domain object instance: RunContext.
    
    """
    return RunContext(
        args=args,
        index=index,
        network=network_id.name,
        node=node_id.index,
        typeof=typeof
    )


def create_run_event(ctx: RunContext, event: str) -> RunEvent:
    """Returns a domain object instance: RunEvent.
    
    """
    return RunEvent(
        event=event,
        network=ctx.network,
        run_index=ctx.index,
        run_typeof=ctx.typeof,
        timestamp=datetime.datetime.now().timestamp()
    )
