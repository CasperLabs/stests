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
    """Encaches domain opbject: Account.
    
    """
    _do_set(account, f"{keyspace.get_key(ctx)}:{keyspace.get_key(account)}")


def set_deploy(ctx, deploy):
    """Encaches domain opbject: Deploy.
    
    """
    _do_set(deploy, f"{keyspace.get_key(ctx)}:{keyspace.get_key(deploy)}")


def set_network(network):
    """Append network information.
    
    """
    _do_set(network, keyspace.get_key(network))


def set_node(node):
    """Encaches domain opbject: Node.
    
    """
    _do_set(node, keyspace.get_key(node))


def set_run_context(ctx):
    """Encaches domain opbject: RunContext.
    
    """
    _do_set(ctx, f"{keyspace.get_key(ctx)}:context")


def set_run_event(ctx, event):
    """Encaches domain opbject: RunEvent.
    
    """
    _do_set(event, f"{keyspace.get_key(ctx)}:{keyspace.get_key(event)}")
