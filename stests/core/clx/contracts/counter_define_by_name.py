import typing

from stests.core.clx import pyclx
from stests.core.clx import defaults
from stests.core.clx.contracts import utils
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import logger


# Type of contract.
TYPE = ContractType.COUNTER_DEFINE

# Wasm file name.
WASM = "counter_define.wasm"

# Named key: contract method: increment.
_NAMED_KEY_INC = "counter_inc"


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 2 member tuple -> (node, deploy_hash).

    """
    return utils.install_contract(src, account, WASM)


def increment(ctx: ExecutionContext, account: Account) -> typing.Tuple[Node, str]:
    """Increments counter by 1.
    
    """
    # Set client.
    node, client  = pyclx.get_client(ctx)

    # Dispatch deploy.
    deploy_hash = client.deploy(
        session_name=_NAMED_KEY_INC,
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: review how these are being assigned
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    logger.log(f"CHAIN :: deploy dispatched :: {deploy_hash} :: COUNTER_DEFINE.increment :: address={account.public_key}")

    return node, deploy_hash


def get_count(node_id: NodeIdentifier, account: Account, block_hash: str) -> int:
    """Queries a node for the current value of the counter under the passed account.
    
    """
    # Set client.
    _, client  = pyclx.get_client(node_id)

    # Query chain global state.
    state = client.queryState(block_hash, account.public_key, "counter/count", "address")

    # Return scalar.
    return state.cl_value.value.i32
