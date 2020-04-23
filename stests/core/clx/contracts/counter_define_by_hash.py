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
_NKEY = "counter"

# Named key: contract method: increment.
_NKEY_INC = "counter_inc"

# State query path.
_QPATH_COUNT = "counter/count"

# Full set of named keys.
NKEYS = [
    _NKEY,
    _NKEY_INC,
]


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str, typing.Dict[str, str]]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 2 member tuple -> (node, deploy_hash).

    """
    return utils.install_contract_by_hash(src, account, WASM)


def increment(src: typing.Any, contract_account: Account, user_account: Account) -> typing.Tuple[Node, str]:
    """Increments counter by 1.
    
    :param src: The source from which a node client will be instantiated.
    :param contract_account: Account under which the contract has been installed.
    :param user_account: A user account invoking the installed contract.

    :returns: 2 member tuple -> (node, deploy_hash).

    """
    # Set client.
    node, client  = pyclx.get_client(ctx)

    # Set named keys of stored contract + slot.
    named_keys = query.get_named_keys(client, contract_account, filter_keys=NKEYS)
    named_keys = {i.name: i.key.hash.hash.hex() for i in named_keys}

    nk_contract = named_keys[_NKEY]
    nk_slot = named_keys[_NKEY_INC]

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
    
    :param node_id: Identifier of node to be queried.
    :param account: Account under which contract was installed.
    :param block_hash: Hash of block at which query will be issued.

    :returns: Current counter value.

    """
    _, client  = pyclx.get_client(node_id)

    state = client.queryState(block_hash, account.public_key, _QPATH_COUNT, "address")

    return state.cl_value.value.i32
