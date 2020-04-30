import typing

from casperlabs_client.abi import ABI

from stests.core.clx import defaults
from stests.core.clx import query
from stests.core.clx import utils
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.chain import NamedKey
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils import logger
from stests.events import EventType



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


def increment(
    src: typing.Any,
    contract_account: Account,
    contract_keys: typing.List[NamedKey],
    user_account: Account,
    ) -> typing.Tuple[Node, str]:
    """Increments counter by 1.
    
    :param src: The source from which a node client will be instantiated.
    :param contract_account: A user account invoking the installed contract.
    :param contract_keys: Named keys associated with installed contract. 
    :param user_account: A user account invoking the installed contract.

    :returns: 2 member tuple -> (node, deploy_hash).

    """
    nk_contract = [i for i in contract_keys if i.name == _NKEY][0]
    nk_inc = [i for i in contract_keys if i.name == _NKEY_INC][0]

    node, _, deploy_hash = utils.dispatch_deploy(
        src,
        user_account,
        from_addr=user_account.public_key,
        session_hash=nk_inc.hash_as_bytes,
        session_args=[ABI.key_hash("counter_key", nk_contract.hash_as_bytes)],
        ) 

    logger.log(f"CHAIN :: {node.label_index} :: {EventType.MONITORING_DEPLOY_DISPATCHED.name} :: COUNTER_DEFINE.increment :: address={user_account.public_key}")

    return node, deploy_hash


def get_count(src: typing.Any, account: Account, block_hash: str=None) -> int:
    """Queries a node for the current value of the counter under the passed account.
    
    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract was installed.
    :param block_hash: Hash of block at which query will be issued.

    :returns: Current counter value.

    """
    state = query.get_state(src, block_hash, account.public_key, "address", _QPATH_COUNT)

    return state.cl_value.value.i32
