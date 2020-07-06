import base64
import os
import pathlib
import time
import typing

from google.protobuf.json_format import MessageToDict

import casperlabs_client
from casperlabs_client import CasperLabsClient
from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core import factory
from stests.core.clx import query
from stests.core.clx.defaults import CLX_TX_FEE
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.core.types.chain import DeployStatus
from stests.core.types.infra import Network
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.core.utils.env import get_var
from stests.core.utils.misc import Timer
from stests.events import EventType



# Max. number of times a deploy will be dispatched.
_MAX_DEPLOY_DISPATCH_ATTEMPTS = 4


def await_deploy_processing(src: typing.Any, deploy_hash: str) -> str:
    """Awaits processing of a dispatched deploy by periodically polling.
    
    :param src: The source from which a node client will be instantiated.
    :param deploy_hash: Hash of previously dispatched deploy.

    :returns: Hash of block in which deploy was included.

    """
    _, client = get_client(src)

    info = client.show_deploy(deploy_hash, wait_for_processed=True)
    if info.status.state not in (DeployStatus.FINALIZED.value, DeployStatus.PROCESSED.value):        
        raise ValueError(f"Deploy processing failure: {info}")

    return info.processing_results[0].block_info.summary.block_hash.hex()


def dispatch_deploy(
    src: typing.Any,
    account: Account,
    from_account_id: bytes = None,
    session: str = None,
    session_args = None,
    session_entry_point: str = None,
    session_hash: str = None,
    session_name: str = None,
    session_uref: str = None,
    transfer_args = None,
    payment_amount=CLX_TX_FEE
    ) -> typing.Tuple[Node, CasperLabsClient, str, float, int]:
    """Dispatches a deploy to target network.  Performs retries upon dispatch failure.  
    
    :param src: The source from which a node client will be instantiated.
    :param account: Account under which deploy will be dispatched.
    :param from_account_id: Purse address that will be used to pay for the deployment.

    :param session: Path to session wasm file.
    :param session_args: Arguments used during deploy processing.
    :param session_entry_point: Name of Entrypoint in contract to call.
    :param session_hash: Hash of a named key associated with account.
    :param session_name: Name of a named key associated with account.
    :param session_uref: Uref of a named key associated with account.

    :param transfer_args: Arguments used when dispatching a transfer.
    :param payment_amount: Gas payment to cover deploy processing costs.

    :returns: 5 member tuple -> (node, client, deploy_hash, dispatch_duration, dispatch_attempts)

    """
    with Timer() as timer:
        attempts = 0
        while attempts < _MAX_DEPLOY_DISPATCH_ATTEMPTS:
            attempts += 1
            node, client = get_client(src)            
            try:
                deploy_hash = client.deploy(
                    # ... account info
                    # algorithm=account.key_algo,
                    from_addr=from_account_id or account.account_id_as_bytes,
                    private_key=account.get_private_key_pem_file(),
                    # ... session info
                    session=session,
                    session_args=session_args,
                    session_entry_point=session_entry_point,
                    session_hash=session_hash,
                    session_name=session_name,
                    # ... transfer info
                    transfer_args=transfer_args,
                    # ... payment info
                    payment_amount=payment_amount,
                )
            except Exception as err:
                if attempts == _MAX_DEPLOY_DISPATCH_ATTEMPTS:
                    raise Exception(f"deploy dispatch failed {_MAX_DEPLOY_DISPATCH_ATTEMPTS} times - {err}")
                log_event(EventType.WFLOW_DEPLOY_DISPATCH_FAILURE, f"try {attempts} failed - retrying", node)
                time.sleep(float(1))
            else:
                break

    return node, client, deploy_hash, timer.elapsed, attempts


def get_client(src: typing.Union[CasperLabsClient, ExecutionContext, Network, NetworkIdentifier, Node, NodeIdentifier]) -> typing.Tuple[Node, CasperLabsClient]:
    """Factory method to return a configured client plus the node with which it is associated.

    :param src: The source from which a network node will be derived.

    :returns: A 2 member tuple: (Node, configured clabs client).
    
    """
    # In some cases calling code already has a client instance, but as
    # method overloading is unsupported in python, code is simplified with a pass through.  
    if isinstance(src, CasperLabsClient):
        return src._node, src

    # Set node. 
    if isinstance(src, Node):
        node = src
    elif isinstance(src, NodeIdentifier):
        node = cache.infra.get_node(src)
    elif isinstance(src, (Network, NetworkIdentifier)):
        node = cache.infra.get_node_by_network(src)
    elif isinstance(src, ExecutionContext):
        node = cache.infra.get_node_by_network_nodeset(
            factory.create_network_id(src.network),
            src.node_index
            )
    else:
        raise ValueError("Cannot derive node from input source.")

    if not node:
        raise ValueError("Network nodeset is empty, therefore cannot dispatch a deploy.")

    # TODO: get node id / client ssl cert ?
    client = CasperLabsClient(
        host=node.host,
        port=node.port,
    )

    # Associate client with node - useful when the client is reused. 
    client._node = node

    return node, client


def get_contract_path(wasm_filename: str) -> pathlib.Path:
    """Returns a path to a smart contract.

    :param wasm_filename: Name of wasm file to be loaded into memory.

    :returns: Path to a wasm blob.
    
    """
    # Return wasm at path specified by env var.
    path = pathlib.Path(get_var("PATH_WASM")) / wasm_filename    
    if path.exists():
        return path

    # Return wasm at python client root.
    path = pathlib.Path(os.path.dirname(casperlabs_client.__file__)) / wasm_filename
    if path.exists():
        return path

    raise ValueError("WASM file could not be found. Verify the STESTS_PATH_WASM env var setting.")


def get_named_keys(src: typing.Any, account: Account, block_hash: str, key_filter: typing.List[str]) -> typing.List[typing.Dict[str, str]]:
    """Queries chain for an account's named keys.

    :param src: The source from which a node client will be instantiated.
    :param account: Target account.
    :param block_hash: Hash of block from which to query.
    :param key_filter: Names of keys of interest.

    :returns: List of 2 member tuples -> (name, hash)

    """
    keys = query.get_named_keys(src, account, block_hash, key_filter)

    return [(i.name, i.key.hash.hash.hex()) for i in keys]


def install_contract(src: typing.Any, account: Account, wasm_filename: str) -> typing.Tuple[Node, str, float, int]:
    """Install a contract under a hash & returns associated named keys.
        
    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.
    :param wasm_filename: Name of wasm file to be installed.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts)
    
    """
    node, _, deploy_hash, dispatch_duration, dispatch_attempts = dispatch_deploy(
        src,
        account,
        session=get_contract_path(wasm_filename),
    )

    return node, deploy_hash, dispatch_duration, dispatch_attempts


def install_contract_by_hash(src: typing.Any, account: Account, wasm_filename: str) -> typing.Tuple[Node, str, float, int]:
    """Install a contract under a hash & returns associated named keys.
        
    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.
    :param wasm_filename: Name of wasm file to be installed.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts)
    
    """
    node, _, deploy_hash, dispatch_duration, dispatch_attempts = dispatch_deploy(
        src,
        account,
        session=get_contract_path(wasm_filename),
        session_args=ABI.args([
            ABI.string_value("target", "hash")
        ])
    )

    return node, deploy_hash, dispatch_duration, dispatch_attempts


def parse_chain_info(info: typing.Any) -> dict:
    """Parses chain information returned from chain over grpc channel.

    :param info: Chain information recieved from chain over RPC channel.

    :returns: Parsed chain information.

    """
    if info is None:
        return dict()

    return _parse_dict(MessageToDict(info))


def _parse_dict(obj: typing.Any, key: str=None) -> typing.Any:
    """Performs a parse over a dictionary deserialized from protobuf layer.
    
    """
    if isinstance(obj, dict):        
        return {k: _parse_dict(v, k) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_parse_dict(i, key) for i in obj]

    # A few integer fields are actually strings in grpc schema.
    try:
        return int(obj)
    except:
        pass
    
    # Auto-encode cryptographic primitives to hex.
    try:
        if 'Hash' in key or \
           'Key' in key or \
           'hash' in key or \
           'uref' in key or \
           key.startswith('sig'):
            return base64.b64decode(obj).hex()
    except:
        pass

    return obj  

