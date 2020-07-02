import typing


from stests.core.clx import utils
from stests.core.clx.contracts import counter_define_by_hash
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.core.types.chain import ContractType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.events import EventType


# Type of contract.
TYPE = ContractType.COUNTER_DEFINE

# Wasm file name.
WASM = "counter_define.wasm"

# Named key: contract method: increment.
_NKEY_INC = "counter_inc"


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str, float, int]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts)

    """
    return utils.install_contract(src, account, WASM)


def increment(src: typing.Any, account: Account) -> typing.Tuple[Node, str, float, int]:
    """Increments counter by 1.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract was installed.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts).
    
    """
    node, _, deploy_hash, dispatch_duration, dispatch_attempts = utils.dispatch_deploy(
        src=src,
        account=account,
        session_name=_NKEY_INC,
    )

    log_event(EventType.WFLOW_DEPLOY_DISPATCHED, f"{deploy_hash} :: COUNTER_DEFINE.increment :: address={account.public_key}", node)

    return node, deploy_hash, dispatch_duration, dispatch_attempts


# Shared function same API.
get_count = counter_define_by_hash.get_count
