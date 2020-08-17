import typing

import dramatiq

from stests import chain
from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext



# Queue to which messages will be dispatched.
_QUEUE = "orchestration.generators.accounts"

# Account index: network faucet.
ACC_NETWORK_FAUCET_INDEX = 0



@dramatiq.actor(queue_name=_QUEUE)
def do_transfer(
    ctx: ExecutionContext,
    cp1_index: int,
    cp2_index: int,
    amount: int = None,
    ):
    # Set counterparties.
    cp1 = _get_account(ctx, cp1_index)
    cp2 = _get_account(ctx, cp2_index)

    # Dispatch tx -> chain.
    chain.transfer(ctx, cp1, cp2, amount)


def _get_account(ctx: ExecutionContext, account_index: int) -> Account:
    """Pulls & returns a cached account.
    
    """
    if account_index == ACC_NETWORK_FAUCET_INDEX:
        network_id = factory.create_network_id(ctx.network)
        network = cache.infra.get_network(network_id)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        return network.faucet
    else:
        return cache.state.get_account_by_index(ctx, account_index)   
