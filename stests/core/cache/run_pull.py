import random
import typing

from stests.core.cache.network_pull import get_network
from stests.core.cache.network_pull import get_nodes
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


def get_run_deploy(dhash: str) -> Deploy:
    """Decaches domain object: Deploy.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    deploys = get_run_deploys(dhash)

    return deploys[-1] if deploys else None


@decache
def get_run_deploys(dhash: str) -> typing.List[Deploy]:
    """Decaches collection of domain objects: Deploy.
    
    :param dhash: A deploy hash.

    :returns: List of matching deploys.

    """    
    return [f"run-deploy*{dhash}*"]


def get_run_network(ctx: RunContext) -> Network:
    """Decaches domain object: Network.
    
    :param ctx: Generator run contextual information.

    :returns: A registered network.

    """
    network_id = factory.create_network_id(ctx.network)

    return get_network(network_id)


def get_run_step(ctx: RunContext) -> RunStep:
    """Decaches domain object: RunStep.
    
    :param ctx: Generator run contextual information.

    :returns: Cached run step information.

    """
    steps = get_run_steps(ctx)
    steps = sorted(steps, key=lambda i: i.ts_start)

    return steps[-1] if steps else None


@decache
def get_run_steps(ctx: RunContext) -> typing.List[RunStep]:
    """Decaches collection of domain objects: RunStep.

    :param ctx: Generator run contextual information.

    :returns: List of run steps.
    
    """
    return [
        "run-step",
        ctx.network,
        ctx.run_type,
        f"R-{str(ctx.run_index).zfill(3)}",
        "*"
        ]


def get_run_transfer(dhash: str) -> Transfer:
    """Decaches domain object: Transfer.
    
    :param dhash: A deploy hash.

    :returns: A run deploy.

    """    
    transfers = get_run_transfers(dhash)

    return transfers[-1] if transfers else None


@decache
def get_run_transfers(dhash: str) -> typing.List[Transfer]:
    """Decaches collection of domain objects: Transfer.
    
    :param dhash: A deploy hash.

    :returns: Matched transfers.

    """    
    return [f"run-transfer*{dhash}*"]
