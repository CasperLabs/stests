import typing

from casperlabs_client.abi import ABI

from stests.core.clx import utils
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventType
from stests.core.types.chain import ContractType
from stests.core.types.orchestration import ExecutionContext



# Type of contract.
TYPE = ContractType.TRANSFER_U512

# Wasm file name.
WASM = "transfer_to_account_u512.wasm"


def transfer(ctx: ExecutionContext, cp1: Account, cp2: Account, amount: int) -> typing.Tuple[Node, str]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: 2 member tuple -> (node, deploy_hash).

    """
    node, _, deploy_hash = utils.dispatch_deploy(
        src=ctx,
        account=cp1,
        session=utils.get_contract_path(WASM),
        session_args=ABI.args([
            ABI.account("account", cp2.public_key_as_bytes),
            ABI.u512("amount", amount),
            ]),
    )

    log_event(NodeEventType.DEPLOY_DISPATCHED, node, message=f"TRANSFER_U512 {amount} CLX from {cp1.public_key[:8]} to {cp2.public_key[:8]}", deploy_hash=deploy_hash)

    return node, deploy_hash
