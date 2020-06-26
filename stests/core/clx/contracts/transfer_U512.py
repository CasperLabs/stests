import typing

from casperlabs_client.abi import ABI

from stests.core.clx import utils
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.chain import ContractType
from stests.core.types.orchestration import ExecutionContext
from stests.events import EventType



# Type of contract.
TYPE = ContractType.TRANSFER_U512


def transfer(ctx: ExecutionContext, cp1: Account, cp2: Account, amount: int) -> typing.Tuple[Node, str, float, int]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts).

    """
    node, _, deploy_hash, dispatch_duration, dispatch_attempts = utils.dispatch_deploy(
        src=ctx,
        account=cp1,
        transfer_args=ABI.args([
            ABI.fixed_list("target", cp2.account_id_as_bytes),
            ABI.u512("amount", amount),
            ]),
    )

    log_event(EventType.MONITORING_DEPLOY_DISPATCHED, f"TRANSFER_U512 {amount} CLX from {cp1.public_key[:8]} to {cp2.public_key[:8]}", node, deploy_hash=deploy_hash)

    return node, deploy_hash, dispatch_duration, dispatch_attempts
