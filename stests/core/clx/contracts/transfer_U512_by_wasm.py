import typing

from casperlabs_client.abi import ABI

from stests.core.clx import pyclx
from stests.core.clx import defaults
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.chain import ContractType
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import logger



# Type of contract.
TYPE = ContractType.TRANSFER_U512

# Wasm file name.
WASM = "transfer_to_account_u512.wasm"

# Name of contract - see use when passed as session-name.
NAME = "transfer_to_account"

# Named keys associated with contract.
NAMED_KEYS = []



def transfer(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int,
    ) -> typing.Tuple[Node, str]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: Hash of dispatched deploy.

    """
    # Set client.
    node, client  = pyclx.get_client(ctx)

    # Dispatch deploy.
    # TODO - consider using generic deploy method ?
    deploy_hash = client.transfer(
        amount=amount,
        target_account_hex=cp2.public_key,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_as_pem_filepath,
        # TODO: review how these are being assigned
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE,
    )

    logger.log(f"CHAIN :: deploy dispatched :: {deploy_hash} :: TRANSFER_U512 :: {amount} CLX :: {cp1.public_key[:8]} -> {cp2.public_key}")

    return node, deploy_hash
