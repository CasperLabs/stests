import json
import random
import subprocess

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
    # Map inputs to pycspr objects.
    cp1 = info.dispatcher.as_pycspr_private_key
    cp2 = cp2.as_pycspr_private_key
    node_client = info.as_pycspr_node_client

    # Set deploy & approve.
    deploy = pycspr.create_native_transfer(
        params=pycspr.create_deploy_parameters(
            account=cp1,
            chain_name=info.network.chain_name
        ),
        amount=amount,
        target=cp2.account_hash,
        correlation_id=random.randint(1, _MAX_TRANSFER_ID)
        )
    deploy.approve(cp1)

    # Dispatch deploy.
    deploy_hash = node_client.deploys.send(deploy)

    if not verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy_hash} :: transfer (native) :: {amount} CSPR :: from {cp1.account_key[:8].hex()} -> {cp2.account_key[:8].hex()} ",
            info.node,
            deploy_hash=deploy_hash,
            )

    return deploy_hash
