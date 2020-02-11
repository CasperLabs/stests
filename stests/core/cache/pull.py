from stests.core.cache import keyspace
from stests.core.cache import stores
from stests.core.cache import utils
from stests.core.domain import AccountType
from stests.core.domain import RunContext



def _do_get(key_ref):
    """Sink function to retrieve instances of domain types.
    
    """
    key = keyspace.get_key(key_ref)
    with stores.get_store() as store:
        return utils.do_get(store, key)


def _do_get1(key):
    """Sink function to retrieve instances of domain types.
    
    """
    with stores.get_store() as store:
        return utils.do_get(store, key)


# Get account information.
get_account = _do_get


def get_account(ctx: RunContext, account_type: AccountType, account_index: int):
    """Append run context information.
    
    """
    if account_type == AccountType.USER:
        account_id = str(account_index).zfill(6)
    else:
        account_id = str(account_index).zfill(2)

    key = f"{ctx.network}.{ctx.run_type}:R-{str(ctx.run_index).zfill(3)}:accounts:{account_type.name}:{account_id}"
    
    return _do_get1(key)


# Get network information.
get_network = _do_get


# Get node information.
get_node = _do_get


# Get node information.
get_run = _do_get
