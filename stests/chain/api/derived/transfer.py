import typing

from stests.chain import constants
from stests.chain import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.orchestration import ExecutionContext



def execute(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int
    ) -> typing.Tuple[Node, str, float, int]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts).

    """
    # TODO: when client supports transfer.
    print(f"{cp1.private_key} :: {cp2.public_key} :: {amount}")
