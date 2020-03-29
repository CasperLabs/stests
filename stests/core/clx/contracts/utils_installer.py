import pathlib
import typing

import casperlabs_client
from casperlabs_client.abi import ABI

from stests.core.clx import defaults
from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.domain import DeployStatus
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
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
    node, client = utils.get_client(node_id or ctx)

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

    logger.log(f"PYCLX :: deploy dispatched -> deploy-hash={deploy_hash} :: {contract.TYPE.name}.install :: account={account.public_key}")

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
    node, client = utils.get_client(node_id or network_id)

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

    logger.log(f"{contract.WASM} :: deploy dispatched -> deploy-hash={deploy_hash}")

    return _get_contract_hash_from_deploy(client, account, contract, deploy_hash)


def _get_contract_hash_from_deploy(
    client: casperlabs_client.CasperLabsClient,
    account: Account,
    contract: typing.Callable,
    deploy_hash: str,
    ) -> str:
    """Returns contract hash of a successfully deployed contract.
    
    """
    # Query chain.
    deploy_info = client.showDeploy(deploy_hash, wait_for_processed=True)
    if deploy_info.status.state not in (DeployStatus.FINALIZED.value, DeployStatus.PROCESSED.value):        
        logger.log_warning(f"{contract.WASM} :: deploy processing failed :: deploy-hash={deploy_hash}")
        raise ValueError(f"Deploy processing failure: {deploy_info}")

    logger.log(f"{contract.WASM} :: deploy processed")

    return _get_contract_hash_from_block(
        client,
        account,
        contract,
        deploy_info.processing_results[0].block_info.summary.block_hash.hex()
        )


def _get_contract_hash_from_block(
    client: casperlabs_client.CasperLabsClient,
    account: Account,
    contract: typing.Callable,
    block_hash: str,
    ) -> str:
    """Returns contract hash of a successfully deployed contract.
    
    """
    q = client.queryState(block_hash, account.public_key, "", keyType="address")
    for nk in q.account.named_keys:
        if nk.name == contract.NAME:
            return nk.key.hash.hash.hex()

    raise ValueError(f"{contract.NAME} contract hash could not be found on-chain")


def _get_contract_path(contract: typing.Callable) -> pathlib.Path:
    """Returns a path to a smart contract.
    
    """
    # TODO: pull from ???
    return pathlib.Path(casperlabs_client.__file__).parent / contract.WASM
