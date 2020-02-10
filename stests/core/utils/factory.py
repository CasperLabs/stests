import datetime
import typing

from stests.core.domain import *
from stests.core.utils import crypto
from stests.core.utils.domain import TypeMetadata



def get_account(
    typeof: AccountType,
    index: int = 1,
    private_key: str = None, 
    public_key: str = None,
    status: AccountStatus = AccountStatus.NEW
    ) -> Account:
    """Returns an account domain object instance.
    
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


def get_network(name_raw: str) -> Network:
    """Returns a network domain object instance.
    
    """
    network_id = get_network_identifier(name_raw)

    return Network(
        faucet=None,
        index=network_id.index,
        name=network_id.name,
        name_raw=name_raw,
        status=NetworkStatus.NULL,
        typeof=network_id.typeof
    )


def get_network_identifier(name_raw: str) -> NetworkIdentifier:
    """Returns a network identifier domain object instance.
    
    """
    name_raw = name_raw.lower()
    index=int(name_raw[3:])
    typeof=name_raw[:3].upper()
    name = f"{typeof}-{str(index).zfill(2)}"

    return NetworkIdentifier(name)


def get_node(
    host: str,
    index: int,
    network_id: NetworkIdentifier,
    port: int,
    typeof: NodeType
    ) -> Node:
    """Returns a node domain object instance.
    
    """
    return Node(
        account=None,
        host=host,
        index=index,
        network=network_id.name,
        port=port,
        typeof=typeof,
        status=NodeStatus.NULL
    )


def get_node_identifier(
    network_id: NetworkIdentifier,
    index: int
    ) -> NodeIdentifier:
    """Returns a node identifier.
    
    """
    return NodeIdentifier(network_id, index)


def get_run_context(
    args: typing.Any,
    index: int,
    network_id: NetworkIdentifier,
    node_id: NodeIdentifier,
    typeof: str
    ) -> RunContext:
    """Domain instance factory: run context.
    
    """
    return RunContext(
        args=args,
        index=index,
        network=network_id.name,
        node=node_id.index,
        typeof=typeof
    )


def get_run_event(ctx: RunContext, event: str) -> RunEvent:
    """Domain instance factory: run event.
    
    """
    return RunEvent(
        event=event,
        network=ctx.network,
        run_index=ctx.index,
        run_typeof=ctx.typeof,
        timestamp=datetime.datetime.now().timestamp()
    )
