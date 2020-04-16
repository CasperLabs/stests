import typing

from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core.clx import pyclx
from stests.core.clx import defaults
from stests.core.domain import Account
from stests.core.domain import ContractType
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger



# Type of contract.
TYPE = ContractType.COUNTER_DEFINE_STORED

# Wasm file name.
WASM = "counter_define.wasm"

# Name of contract - see use when passed as session-name.
NAME = "counter"

# Flag indicating whether this contract can be installed under a single account and invoked by other accounts.
IS_SINGLETON = True


# Named key: contract.
NAMED_KEY_COUNTER = "counter"

# Named key: slot.
NAMED_KEY_COUNTER_INC = "counter_inc"

# Full set of named keys.
NAMED_KEYS = [
    NAMED_KEY_COUNTER,
    NAMED_KEY_COUNTER_INC,
]


def increment(ctx: ExecutionContext, account: Account) -> typing.Tuple[Node, str]:
    """Increments counter previously installed under an account.
    
    """
    # Set client.
    node, client  = pyclx.get_client(ctx)

    # Set named keys of stored contract + slot.
    nk_contract = cache.infra.get_named_key(ctx.network, TYPE, NAMED_KEY_COUNTER)
    nk_slot = cache.infra.get_named_key(ctx.network, TYPE, NAMED_KEY_COUNTER_INC)
    if nk_contract is None or nk_slot is None:
        raise ValueError(f"{WASM} has not been installed upon chain.")

    # Dispatch deploy.
    deploy_hash = client.deploy(
        session_hash=nk_contract.hash_as_bytes,
        session_args=[
            ABI.key_hash("counter_key", nk_slot.hash_as_bytes),
            ],
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
    _, client  = pyclx.get_client(node_id)

    # Query chain global state.
    state = client.queryState(block_hash, account.public_key, "counter/count", "address")

    # Return scalar.
    return state.cl_value.value.i32
