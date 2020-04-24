import typing

from stests.core.clx import pyclx
from stests.core.clx.contracts import counter_define_by_hash
from stests.core.clx.contracts import utils
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeEventType
from stests.core.types.infra import NodeIdentifier
from stests.core.utils import logger


# Type of contract.
TYPE = ContractType.COUNTER_DEFINE

# Wasm file name.
WASM = "counter_define.wasm"

# Named key: contract method: increment.
_NKEY_INC = "counter_inc"


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 2 member tuple -> (node, deploy_hash)

    """
    return utils.install_contract(src, account, WASM)


def increment(src: typing.Any, account: Account) -> typing.Tuple[Node, str]:
    """Increments counter by 1.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract was installed.

    :returns: 2 member tuple -> (node, deploy_hash).
    
    """
    node, _, deploy_hash = utils.dispatch_deploy(
        src=src,
        account=account,
        session_name=_NKEY_INC,
    )

    logger.log(f"CHAIN :: {node.label_index} :: event :: 0000 :: {NodeEventType.DEPLOY_DISPATCHED.name} :: COUNTER_DEFINE.increment :: address={account.public_key}")

    return node, deploy_hash


# Shared function same API.
get_count = counter_define_by_hash.get_count
