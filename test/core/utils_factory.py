import datetime
import random
import typing

from stests.core.domain import Account
from stests.core.domain import AccountStatus
from stests.core.domain import AccountType
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import Network
from stests.core.domain import NetworkStatus
from stests.core.domain import NetworkType
from stests.core.domain import Node
from stests.core.domain import NodeStatus
from stests.core.domain import NodeType

from stests.core.domain import RunContext
from stests.core.domain import RunEvent
from stests.core.domain import RunInfo

from stests.core.utils import crypto
from stests.core.utils import factory



def get_account(typeof: AccountType=None) -> Account:
    """Factory function that returns a test account.
    
    """
    return factory.get_account(
        status=random.choice(list(AccountStatus)),
        typeof=typeof or random.choice(list(AccountType))
    )


def get_deploy() -> Deploy:
    """Factory function that returns a test deploy.
    
    """
    return Deploy(
        hash_id="6ff843ba685842aa82031d3f53c48b66326df7639a63d128974c5c14f31a0f33343a8c65551134ed1ae0f2b0dd2bb495dc81039e3eeb0aa1bb0388bbeac29183",
        status=random.choice(list(DeployStatus))
    )


def get_network() -> Network:
    """Factory function that returns a test network.
    
    """
    index=1
    typeof=NetworkType.LOC

    return Network(
        faucet=get_account(AccountType.FAUCET),
        index=index,
        name=f"{typeof.name}-{str(index).zfill(2)}",
        name_raw=f"{typeof.name.lower()}{index}",
        status=random.choice(list(NetworkStatus)),
        typeof=random.choice(list(NetworkType)),
    )


def get_node() -> Node:
    """Factory function that returns a test node.
    
    """
    return Node(
        account=get_account(AccountType.BOND),
        host="localhost",
        index=1,
        network="LOC-01",
        port=40400,
        status=random.choice(list(NodeStatus)),
        typeof=random.choice(list(NodeType)),
    )


def get_run_context() -> RunContext:
    """Factory function that returns a test run context.
    
    """
    return RunContext(
        args=None,
        index=1,
        network="LOC-01",
        node=1,
        typeof="WG-XXX"
        )


def get_run_event() -> RunEvent:
    """Factory function that returns a test run event.
    
    """
    return RunEvent(
        name="on_wg_event",
        timestamp=datetime.datetime.now().timestamp(),
        run_info=get_run_info()
    )


def get_run_info() -> RunInfo:
    """Factory function that returns a test run info.
    
    """
    return RunInfo(
        index=1,
        network="LOC-01",
        node=1,
        typeof="WG-XXX"
    )


# Map: domain type to factory function.
FACTORIES: typing.Dict[typing.Type, typing.Callable] = {
    Account: get_account,
    Deploy: get_deploy,
    Network: get_network,
    Node: get_node,
    RunContext: get_run_context,
    RunEvent: get_run_event,
    RunInfo: get_run_info
}


def get_instance(dcls: typing.Type) -> typing.Any:
    """Factory function that returns a test domain object.
    
    """
    try:
        factory = FACTORIES[dcls]
    except KeyError:
        raise ValueError("Unsupported domain type: {}".format(dcls))
    else:
        return factory()
