import typing

from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core.clx.contracts import utils
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.chain import ContractType
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import logger



# Type of contract.
TYPE = ContractType.TRANSFER_U512_STORED

# Wasm file name.
WASM = "transfer_to_account_u512_stored.wasm"

# Name of contract - see use when passed as session-name.
_NAMED_KEY = "transfer_to_account"

# Named keys associated with contract.
NAMED_KEYS = [
    _NAMED_KEY,
]


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str, typing.Dict[str, str]]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 3 member tuple -> (node, deploy_hash, named_keys).

    """
    return utils.install_contract(src, account, WASM, NAMED_KEYS)


def transfer(ctx: ExecutionContext, cp1: Account, cp2: Account, amount: int) -> typing.Tuple[Node, str]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: Hash of dispatched deploy.

    """
    # Set named key associated with contract.
    named_key = cache.infra.get_account_named_key(ctx.network, TYPE, _NAMED_KEY)
    if named_key is None:
        raise ValueError(f"{WASM} has not been installed upon chain.")

    # Dispatch deploy.
    node, _, deploy_hash = utils.dispatch_deploy(
        src=ctx,
        account=cp1,
        session_hash=named_key.hash_as_bytes,
        session_args=ABI.args([
            ABI.account("address", cp2.public_key),
            ABI.big_int("amount", amount),
            ]),

    )

    logger.log(f"CHAIN :: deploy dispatched :: {deploy_hash} :: TRANSFER_U512_STORED :: {amount} CLX :: {cp1.public_key[:8]} -> {cp2.public_key}")

    return node, deploy_hash
