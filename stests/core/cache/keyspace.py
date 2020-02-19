import typing

from stests.core.cache.identifiers import IDENTIFIER_SET

from stests.core.cache.identifiers import AccountIdentifier
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.cache.identifiers import NodeIdentifier
from stests.core.cache.identifiers import RunIdentifier

from stests.core.domain import Account
from stests.core.domain import Transfer
from stests.core.domain import AccountType
from stests.core.domain import Block
from stests.core.domain import Deploy
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



# Map: global collection -> key
_GLOBAL_COLLECTIONS = {
    typing.List[Network]: "network:*"
}


def get_key(obj):
    """Returns key derived from a domain type instance.
    
    """
    try:
        return _GLOBAL_COLLECTIONS[obj]
    except (KeyError, TypeError):
        pass

    if isinstance(obj, IDENTIFIER_SET):
        return _get_identifier_key(obj)

    if isinstance(obj, tuple) and len(obj) == 2:
        return _get_collection_key(obj)

    return _get_item_key(obj)


def _get_identifier_key(obj):
    """Returns a cache identifier key.
    
    """
    if isinstance(obj, AccountIdentifier):
        return f"{_get_identifier_key(obj.run)}:{str(obj.index).zfill(6)}"

    if isinstance(obj, NetworkIdentifier):
        return f"{obj.name}"

    if isinstance(obj, NodeIdentifier):
        return f"{obj.network.name}:N-{str(obj.index).zfill(4)}"

    if isinstance(obj, RunIdentifier):
        return f"{obj.network.name}:{obj.type}:R-{str(obj.index).zfill(3)}"


def _get_item_key(obj):
    """Returns an item key.
    
    """
    if isinstance(obj, Account):
        return f"{str(obj.index).zfill(6)}"

    if isinstance(obj, Block):
        return f"{obj.timestamp}.{obj.bhash}"

    if isinstance(obj, Deploy):
        return f"{obj.ts_dispatched}.{obj.dhash}"

    if isinstance(obj, Network):
        return obj.name

    if isinstance(obj, Node):
        return f"{obj.network}:N-{str(obj.index).zfill(4)}"

    if isinstance(obj, RunContext):
        return f"{obj.network_name}:{obj.run_type}:R-{str(obj.run_index).zfill(3)}"

    if isinstance(obj, RunEvent):
        return f"{obj.timestamp}.{obj.event}"

    if isinstance(obj, Transfer):
        return f"{obj.asset.lower()}:{obj.dhash}"


def _get_collection_key(obj):
    """Returns a collection key.
    
    """
    id, type = obj
    if isinstance(id, NetworkIdentifier) and type == typing.List[Node]:
        return f"node:{id.name}:N-*"

    raise ValueError("Unsupported collection")
