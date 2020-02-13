import typing

from stests.core.cache.identifiers import IDENTIFIER_SET
from stests.core.cache.identifiers import NetworkIdentifier
from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import Deploy
from stests.core.domain import Network
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



# Map: global collection -> key
_GLOBAL_COLLECTIONS = {
    typing.List[Network]: "global.network:*"
}


def get_key(obj):
    """Returns key derived from a domain type instance.
    
    """
    if isinstance(obj, IDENTIFIER_SET):
        return obj.key

    if obj in _GLOBAL_COLLECTIONS:
        return _GLOBAL_COLLECTIONS[obj]

    if isinstance(obj, tuple) and len(obj) == 2:
        return _get_collection_key(obj)

    return _get_item_key(obj)


def _get_item_key(obj):
    """Returns an item key.
    
    """
    if isinstance(obj, Account):
        zfill = 6 if obj.typeof == AccountType.USER else 2
        return f"accounts:{obj.typeof.name}:{str(obj.index).zfill(zfill)}"

    if isinstance(obj, Deploy):
        return f"deploys:{obj.ts_dispatched}.{obj.hash_id}"

    if isinstance(obj, Network):
        return f"global.network:{obj.name}"

    if isinstance(obj, Node):
        return f"global.node:{obj.network}:N-{str(obj.index).zfill(4)}"

    if isinstance(obj, RunContext):
        return f"{obj.network}.{obj.typeof}:R-{str(obj.index).zfill(3)}"

    if isinstance(obj, RunEvent):
        return f"events:{obj.timestamp}.{obj.event}"


def _get_collection_key(obj):
    """Returns a collection key.
    
    """
    id, type = obj
    if isinstance(id, NetworkIdentifier) and type == typing.List[Node]:
        return f"global.node:{id.name}:N-*"

    raise ValueError("Unsupported collection")