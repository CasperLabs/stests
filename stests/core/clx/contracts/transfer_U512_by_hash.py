import typing

from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core.clx import pyclx
from stests.core.clx import defaults
from stests.core.clx.contracts import utils
from stests.core.clx.query import get_account_balance
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.chain import ContractType
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import logger



# Type of contract.
TYPE = ContractType.TRANSFER_U512_STORED

# Wasm file name.
WASM = "transfer_to_account_u512_stored.wasm"


# Flag indicating whether this contract can be installed under a single account and invoked by other accounts.
IS_SINGLETON = True

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


def transfer(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int,
    ):
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: Hash of dispatched deploy.

    """
    # Set client.
    node, client  = pyclx.get_client(ctx)

    # Set named key associated with contract.
    named_key = cache.infra.get_account_named_key(ctx.network, TYPE, _NAMED_KEY)
    if named_key is None:
        raise ValueError(f"{WASM} has not been installed upon chain.")

    # Set args.
    session_args = ABI.args([
        ABI.account("address", cp2.public_key),
        ABI.big_int("amount", amount),
        ])

    # Dispatch deploy.
    deploy_hash = client.deploy(
        session_hash=named_key.hash_as_bytes,
        session_args=session_args,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_as_pem_filepath,
        # TODO: review how these are being assigned
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE,
    )

    logger.log(f"CHAIN :: deploy dispatched :: {deploy_hash} :: TRANSFER_U512_STORED :: {amount} CLX :: {cp1.public_key[:8]} -> {cp2.public_key}")

    return node, deploy_hash


def refund(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int = None,
    ) -> typing.Tuple[Node, str, int]:
    """Executes a refund between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be refunded.

    :returns: 3 member tuple: dispatch node, deploy hash, refund amount.

    """
    # If amount is unspecified, set amount to entire balance.
    if amount is None:
        balance = get_account_balance(ctx, cp1) 
        amount = balance - defaults.CLX_TX_FEE
    
    # Escape if cp1 has insufficient funds.
    if amount <= 0:
        logger.log_warning(f"Counter party 1 (account={cp1.index}) does not have enough CLX to pay refund transaction fee, balance={balance}.")
        return

    (node, deploy_hash) = transfer(ctx, cp1, cp2, amount)

    return node, deploy_hash, amount
