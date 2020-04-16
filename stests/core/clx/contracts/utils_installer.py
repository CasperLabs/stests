import pathlib
import typing

import casperlabs_client
from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core.clx import pyclx
from stests.core.clx import defaults
from stests.core.clx import query
from stests.core.domain import Account
from stests.core.domain import DeployStatus
from stests.core.domain import NamedKey
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger



def install_named(
    ctx: ExecutionContext,
    account: Account,
    contract: typing.Callable,
    node_id: NodeIdentifier = None,
    ) -> str:
    """Installs a named smart contract upon a chain.

    :param ctx: Execution context information.
    :param account: Account under which contract will be installed - defaults to network faucet account.
    :param contract: Contract to be installed.
    :param node_id: Identifier of node to which deploys will be dispatched.

    :returns: Contract hash (in hex format).

    """
    # Set client.
    node, client = pyclx.get_client(node_id or ctx)

    # Set deploy args.
    session = _get_contract_path(contract)

    # Dispatch deploy.
    try:
        deploy_hash = client.deploy(
            session=session,
            from_addr=account.public_key,
            private_key=account.private_key_as_pem_filepath,
            # TODO: review how these are being assigned
            payment_amount=defaults.CLX_TX_FEE,
            gas_price=defaults.CLX_TX_GAS_PRICE
        )
    except casperlabs_client.casperlabs_client.InternalError as err:
        if err.details.index("UNAVAILABLE") >= 0:
            raise IOError("Node is unreachable therefore contract cannot be deployed.")
        raise err

    logger.log(f"CHAIN :: deploy dispatched -> deploy-hash={deploy_hash} :: {contract.TYPE.name}.install :: account={account.public_key}")

    return (node, deploy_hash)


def install_singleton(
    network_id: typing.Union[Network, NetworkIdentifier],
    account: Account,
    contract: typing.Callable,
    node_id: NodeIdentifier = None,
    ) -> str:
    """Installs a smart contract upon a chain & returns it's contract hash.

    :param network_id: Identifier of network into which contract is being installed.
    :param account: Account under which contract will be installed - defaults to network faucet account.
    :param contract: Contract to be installed.
    :param node_id: Identifier of node to which deploys will be dispatched.

    :returns: Contract hash (in hex format).

    """
    # Set client.
    node, client = pyclx.get_client(node_id or network_id)

    # Set deploy args.
    session = _get_contract_path(contract)
    session_args = ABI.args([
        ABI.string_value("target", "hash")
        ])

    # Dispatch deploy.
    try:
        deploy_hash = client.deploy(
            session=session,
            session_args=session_args,
            from_addr=account.public_key,
            private_key=account.private_key_as_pem_filepath,
            # TODO: review how these are being assigned
            payment_amount=defaults.CLX_TX_FEE,
            gas_price=defaults.CLX_TX_GAS_PRICE
        )
    except casperlabs_client.casperlabs_client.InternalError as err:
        if err.details.index("UNAVAILABLE") >= 0:
            raise IOError("Node is unreachable therefore contract cannot be deployed.")
        raise err

    logger.log(f"{contract.WASM} :: deploy dispatched -> {deploy_hash}")

    # Await deploy processing.
    deploy_info = client.showDeploy(deploy_hash, wait_for_processed=True)
    if deploy_info.status.state not in (DeployStatus.FINALIZED.value, DeployStatus.PROCESSED.value):        
        logger.log_warning(f"{contract.WASM} :: deploy processing failed :: deploy-hash={deploy_hash}")
        raise ValueError(f"Deploy processing failure: {deploy_info}")

    # Set hash of block in which deploy was processed.
    block_hash = deploy_info.processing_results[0].block_info.summary.block_hash.hex()
    logger.log(f"{contract.WASM} :: deploy processed -> block={block_hash}")

    # Set named keys associated with contract.
    _set_contract_named_keys(account, contract, node, client, block_hash)


def _set_contract_named_keys(account, contract, node, client, block_hash):
    """Stores contract related named keys.
    
    """
    for key in query.get_account_named_keys(client, account, block_hash, contract.NAMED_KEYS):
        _set_contract_named_key(account, contract, node, client, block_hash, key)


def _set_contract_named_key(account, contract, node, client, block_hash, key):
    """Stores contract related named key.
    
    """
    key = factory.create_account_named_key(
        account,
        contract.TYPE,
        key.name,
        node.network,
        key.key.hash.hash.hex(),
    )
    cache.infra.set_named_key(key)
    logger.log(f"{contract.WASM} :: named key cached -> {key.name}")


def _get_contract_path(contract: typing.Callable) -> pathlib.Path:
    """Returns a path to a smart contract.
    
    """
    # TODO: pull from ???
    return pathlib.Path(casperlabs_client.__file__).parent / contract.WASM
