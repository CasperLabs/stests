import typing

from stests.core.clx import defaults
from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.domain import ContractType
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger


# Type of contract.
TYPE = ContractType.COUNTER_DEFINE

# Wasm file name.
WASM = "counter_define.wasm"

# Name of contract - see use when passed as session-name.
NAME = "counter"

# Flag indicating whether this contract can be installed under a single account and invoked by other accounts.
IS_SINGLETON = False

# Named keys associated with contract.
NAMED_KEYS = []


def increment(ctx: ExecutionContext, account: Account) -> typing.Tuple[Node, str]:
    """Increments counter previously installed under an account.
    
    """
    # Set client.
    node, client  = utils.get_client(ctx)

    # Dispatch deploy.
    deploy_hash = client.deploy(
        session_name="counter_inc",
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: review how these are being assigned
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    logger.log(f"CHAIN :: deploy dispatched :: {deploy_hash} :: COUNTER_DEFINE.increment :: address={account.public_key}")

    return (node, deploy_hash)


def get_count(node_id: NodeIdentifier, account: Account, block_hash: str) -> int:
    """Queries a node for the current value of the counter under the passed account.
    
    """
    # Set client.
    node, client  = utils.get_client(node_id)

    # Query chain global state.
    state = client.queryState(block_hash, account.public_key, "counter/count", "address")

    # Return scalar.
    return state.cl_value.value.i32
