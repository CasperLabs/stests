import pathlib
import typing

import casperlabs_client
from casperlabs_client import CasperLabsClient
from casperlabs_client.abi import ABI


from stests.core.clx import query
from stests.core.clx.pyclx import get_client
from stests.core.clx.defaults import CLX_TX_FEE
from stests.core.clx.defaults import CLX_TX_GAS_PRICE

from stests.core.types.chain import Account
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import Node

# from_addr: bytes = None,
# gas_price: int = 10,

# public_key: str = None,
# private_key: str = None,

# payment: str = None,
# payment_amount: int = None,
# payment_hash: bytes = None,
# payment_name: str = None,
# payment_uref: bytes = None,
# payment_args: bytes = None,

# session: str = None,
# session_hash: bytes = None,
# session_name: str = None,
# session_uref: bytes = None,
# session_args: bytes = None,

# ttl_millis: int = 0,
# dependencies=None,
# chain_name: str = None,


def await_deploy_processing(src, deploy_hash: str) -> str:
    """Awaits processing of a dispatched deploy by periodically polling.
    
    :param src: The source from which a node client will be instantiated.
    :param deploy_hash: Hash of previously dispatched deploy.

    :returns: Hash of block in which deploy was included.

    """
    _, client = get_client(src)

    info = client.showDeploy(deploy_hash, wait_for_processed=True)
    if info.status.state not in (DeployStatus.FINALIZED.value, DeployStatus.PROCESSED.value):        
        raise ValueError(f"Deploy processing failure: {info}")

    return info.processing_results[0].block_info.summary.block_hash.hex()
    

def dispatch_deploy(
    src,
    account: Account,
    session: str = None,
    session_args = None,
    session_hash: str = None,
    session_name: str = None,
    session_uref: str = None,
    ) -> typing.Tuple[Node, CasperLabsClient, str]:
    """Dispatches a deploy to target network.
    
    :param src: The source from which a node client will be instantiated.
    :param account: Account under which deploy will be dispatched.
    :param session: Path to session wasm file.
    :param session_args: Arguments used during deploy processing.
    :param session_hash: Hash of a named key associated with account.
    :param session_name: Name of a named key associated with account.
    :param session_uref: Uref of a named key associated with account.

    :returns: 3 member tuple -> (node, client, deploy_hash)

    """
    node, client = get_client(src)
    try:
        deploy_hash = client.deploy(
            session=session,
            session_args=session_args,
            session_hash=session_hash,
            session_name=session_name,
            session_uref=session_uref,

            from_addr=account.public_key,
            private_key=account.private_key_as_pem_filepath,

            # TODO: review how these are being assigned
            payment_amount=CLX_TX_FEE,
            gas_price=CLX_TX_GAS_PRICE
        )
    except casperlabs_client.casperlabs_client.InternalError as err:
        if err.details.index("UNAVAILABLE") >= 0:
            raise IOError("Deploy dispatch error: unreachable node")
        raise err

    return node, client, deploy_hash


def get_contract_path(wasm_filename: str) -> pathlib.Path:
    """Returns a path to a smart contract.

    :param wasm_filename: Name of wasm file to be loaded into memory.

    :returns: Path to a wasm blob.
    
    """
    # TODO: pull from ???
    return pathlib.Path(casperlabs_client.__file__).parent / wasm_filename


def get_named_keys(src, account, block_hash, key_filter) -> typing.List[typing.Dict[str, str]]:
    """Queries chain for an account's named keys.

    :param src: The source from which a node client will be instantiated.
    :param account: Target account.
    :param block_hash: Hash of block from which to query.
    :param key_filter: Names of keys of interest.

    :returns: List of 2 member tuples -> (name, hash)

    """
    keys = query.get_account_named_keys(src, account, block_hash, key_filter)

    return [(i.name, i.key.hash.hash.hex()) for i in keys]


def install_contract(src: typing.Any, account: Account, wasm_filename: str, key_filter: typing.List[str]=[]) -> typing.Tuple[Node, str]:
    """Install a contract under a hash & returns associated named keys.
        
    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.
    :param wasm_filename: Name of wasm file to be installed.
    :param key_filter: Names of keys of interest.

    :returns: 3 member tuple -> (node, deploy_hash, named_keys)
    
    """
    session=get_contract_path(wasm_filename)
    session_args = None if not key_filter else ABI.args([
            ABI.string_value("target", "hash")
        ])

    node, client, deploy_hash = dispatch_deploy(
        src,
        account,
        session=session,
        session_args=session_args
    )
    if not key_filter:
        return node, deploy_hash, []

    block_hash = await_deploy_processing(client, deploy_hash)
    named_keys = get_named_keys(client, account, block_hash, key_filter)

    return node, deploy_hash, named_keys
