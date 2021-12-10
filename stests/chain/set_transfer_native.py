import random

import pycspr 

from stests.core.logging import log_event
from stests.chain.utils import execute_api
from stests.chain.utils import DeployDispatchInfo
from stests.core.types.chain import Account
from stests.events import EventType


# Maximum value of a transfer ID.
_MAX_TRANSFER_ID = (2 ** 63) - 1


@execute_api("transfer", EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, cp2: Account, amount: int, verbose: bool = True) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param info: Standard information required to dispatch deploy.
    :param cp2: Account information of counter party 2.
    :param amount: Amount (in motes) to be transferred.
    :param verbose: Flag inidcating whether event will be logged.
    :returns: Dispatched deploy hash.

    """
    # Set counter-parties.
    cp1: pycspr.types.PrivateKey = info.dispatcher.as_pycspr_private_key
    cp2: pycspr.types.PublicKey = cp2.as_pycspr_public_key

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=pycspr.create_deploy_parameters(
            account=cp1,
            chain_name=info.network.chain_name
        ),
        amount=amount,
        target=cp2.account_key,
        correlation_id=random.randint(1, _MAX_TRANSFER_ID)
        )

    # Set approval.
    deploy.approve(cp1)

    # Dispatch.
    info.node.dispatch_deploy(deploy)

    if verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy.hash.hex()} :: transfer (native) :: {amount} CSPR :: from {cp1.account_key[:8].hex()} -> {cp2.account_key[:8].hex()} ",
            info.node,
            deploy_hash=deploy.hash,
            )

    return deploy.hash.hex()
