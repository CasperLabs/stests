from stests.core.cache import keyspace
from stests.core.cache import stores
from stests.core.cache import utils



def _do_set(instance, key):
    """Sink function to push instances of domain types.
    
    """
    with stores.get_store() as store:
        utils.do_set(store, key, instance)


# Append account information.
def set_account(ctx, account):
    """Append account information.
    
    """
    _do_set(account, f"{keyspace.get_key(ctx)}:{keyspace.get_key(account)}")


def set_network(network):
    """Append network information.
    
    """
    _do_set(network, keyspace.get_key(network))


def set_node(node):
    """Append network information.
    
    """
    _do_set(node, keyspace.get_key(node))


def set_run_context(ctx):
    """Append run context information.
    
    """
    _do_set(ctx, f"{keyspace.get_key(ctx)}:context")


def set_run_event(ctx, event):
    """Append run event information.
    
    """
    _do_set(event, f"{keyspace.get_key(ctx)}:{keyspace.get_key(event)}")
