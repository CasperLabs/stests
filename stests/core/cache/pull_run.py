import random
import typing

from stests.core.cache.pull_network import get_network
from stests.core.cache.pull_network import get_nodes
from stests.core.cache.utils import decache
from stests.core.domain import *
from stests.core.utils import factory



@decache
def get_account(account_id: AccountIdentifier) -> Account:
    """Decaches domain object: Account.

    :param account_id: An account identifier.

    :returns: A cached account.

    """
    run = account_id.run

    return [
        "run-account",
        run.network.name,
        run.type,
        f"R-{str(run.index).zfill(3)}",
        f"{str(account_id.index).zfill(6)}"
    ]


def get_run_account(ctx: RunContext, index: int) -> Account:
    """Decaches domain object: Account.
    
    :param ctx: Generator run contextual information.
    :param index: Run specific account index. 

    :returns: A cached account.

    """
    return get_account(factory.create_account_id(
        index,
        ctx.network,
        ctx.run,
        ctx.run_type
        ))


def get_run_network(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Generator run contextual information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return get_network(network_id)


def get_run_node(ctx: RunContext) -> Node:
    """Decaches domain object: Node.
    
    :param ctx: Generator run contextual information.

    :returns: A registered node.

    """
    # Pull healthy nodes.
    network_id = factory.create_network_id(ctx.network)
    nodes = [i for i in get_nodes(network_id) if i.status == NodeStatus.HEALTHY] 
    if not nodes:
        raise ValueError(f"Network {network_id.name} has no registered healthy nodes.")
    
    # Select random if node index unspecified.
    if ctx.node <= 0 or ctx.node is None:
        return random.choice(nodes)

    # Select specific with fallback to random.
    try:
        return nodes[ctx.node - 1]
    except IndexError:
        return random.choice(nodes)


@decache
def get_run_deploy_entities(dhash: str) -> typing.List[typing.Union[Deploy, Transfer]]:
    """Decaches all deploys and/or transfers relating to a particular run/deploy combination.
    
    :param dhash: A deploy hash.

    :returns: List of matching deploys and/or transfers.

    """    
    return [f"run-*{dhash}*"]


@decache
def get_run_deploys(dhash: str) -> typing.List[Deploy]:
    """Decaches all deploys relating to a particular run/deploy combination.
    
    :param dhash: A deploy hash.

    :returns: List of matching deploys.

    """    
    return [f"run-deploy*{dhash}*"]


def get_run_deploy(dhash: str) -> typing.List[Deploy]:
    """Decaches a run deploy.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    all = get_run_deploys(dhash)

    return all[-1] if all else None


def get_run_step_current(network, run, run_type) -> RunStep:
    """Decaches domain object: RunStep.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run step information.

    """
    all = get_run_steps(network, run, run_type)
    all = sorted(all, key=lambda i: i.timestamp)

    return all[-1] if all else None


@decache
def get_run_context(network, run_index, run_type) -> RunContext:
    """Decaches domain object: RunContext.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run context information.

    """
    return [
        "run-context",
        network,
        run_type,
        f"R-{str(run_index).zfill(3)}"
    ]


@decache
def get_run_steps(network, run, run_type) -> typing.List[RunStep]:
    """Decaches domain objects: RunStep.

    :returns: List of run steps.
    
    """
    return [
        "run-step",
        network,
        run_type,
        f"R-{str(run).zfill(3)}",
        "*"
        ]
