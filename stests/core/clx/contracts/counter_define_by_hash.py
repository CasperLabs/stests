import typing

from casperlabs_client.abi import ABI

from stests.core.clx import pyclx
from stests.core.clx import query
from stests.core.clx import defaults
from stests.core.clx.contracts import utils
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import logger



# Type of contract.
TYPE = ContractType.COUNTER_DEFINE_STORED

# Wasm file name.
WASM = "counter_define.wasm"

# Named key: contract.
_NAMED_KEY = "counter"

# Named key: contract method: increment.
_NAMED_KEY_INC = "counter_inc"

# Full set of named keys.
NAMED_KEYS = [
    _NAMED_KEY,
    _NAMED_KEY_INC,
]


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str, typing.Dict[str, str]]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 3 member tuple -> (node, deploy_hash, named_keys).

    """
    return utils.install_contract(src, account, WASM, NAMED_KEYS)


def increment(src: typing.Any, contract_account: Account, user_account: Account) -> typing.Tuple[Node, str]:
    """Increments counter by 1.
    
    :param src: The source from which a node client will be instantiated.
    :param contract_account: Account under which the contract has been installed.
    :param user_account: A user account invoking the installed contract.

    :returns: 2 member tuple -> (node, deploy_hash)

    """
    # Set client.
    node, client  = pyclx.get_client(ctx)

    # Set named keys of stored contract + slot.
    named_keys = query.get_account_named_keys(client, contract_account, filter_keys=NAMED_KEYS)
    named_keys = {i.name: i.key.hash.hash.hex() for i in named_keys}

    nk_contract = named_keys[_NAMED_KEY]
    nk_slot = named_keys[_NAMED_KEY_INC]

    if nk_contract is None or nk_slot is None:
        raise ValueError(f"{WASM} has not been installed upon chain.")

    # Dispatch deploy.
    deploy_hash = client.deploy(
        session_hash=nk_contract.hash_as_bytes,
        session_args=[
            ABI.key_hash("counter_key", nk_slot.hash_as_bytes),
            ],
        from_addr=user_account.public_key,
        private_key=user_account.private_key_as_pem_filepath,
        # TODO: review how these are being assigned
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    # Set client.
    _, client  = pyclx.get_client(ctx)

    _, _, deploy_hash = utils.dispatch_deploy(
        client,
        user_account,
        session_hash=nk_contract.hash_as_bytes,
        session_args=[
                ABI.key_hash("counter_key", nk_slot.hash_as_bytes),
            ],
        ) 

    logger.log(f"CHAIN :: deploy dispatched :: {deploy_hash} :: COUNTER_DEFINE.increment :: address={user_account.public_key}")

    return node, deploy_hash


def get_count(node_id: NodeIdentifier, account: Account, block_hash: str) -> int:
    """Queries a node for the current value of the counter under the passed account.
    
    :returns: Current value of counter.

    """
    # Set client.
    _, client  = pyclx.get_client(node_id)

    # Query chain global state.
    state = client.queryState(block_hash, account.public_key, "counter/count", "address")

    # Return scalar.
    return state.cl_value.value.i32
