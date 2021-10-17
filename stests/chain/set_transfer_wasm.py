import pycspr

from pycspr.types import StorageKeyType
from stests.chain import constants
from stests.chain import set_deploy
from stests.chain.utils import execute_api
from stests.chain.utils import execute_cli
from stests.chain.utils import DeployDispatchInfo
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.core.types.infra import Network
from stests.core.types.infra import Node
from stests.events import EventType
from stests.core.utils import paths



# Method upon client to be invoked.
_CLIENT_METHOD = "put-deploy"

# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "transfer_to_account_u512.wasm"


@execute_api("transfer-wasm", EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(info: DeployDispatchInfo, cp2: Account, amount: int, verbose: bool = True) -> str:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param info: Standard information required to dispatch deploy.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param verbose: Flag inidcating whether event will be logged.
    :returns: Dispatched deploy hash.

    """
    cp1 = info.dispatcher
    deploy = _get_deploy(info, cp2, amount)

    deploy_hash = set_deploy.execute(
        info.network,
        info.node,
        info.dispatcher,
        _CONTRACT_FNAME,
        [
            "--session-arg", f"amount:u512='{amount}'",
            "--session-arg", f"target:account_hash='account-hash-{cp2.account_hash}'",
        ]
    )

    if verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy_hash} :: transfer (wasm) :: {amount} CSPR :: from {cp1.account_key[:8]} -> {cp2.account_key[:8]} ",
            info.node,
            deploy_hash=deploy_hash,
            )

    return deploy_hash


def _get_deploy(info: DeployDispatchInfo, cp2: Account, amount: int) -> pycspr.types.Deploy:
    """Returns delegation deploy to be dispatched to a node.

    """
    cp1: pycspr.types.PrivateKey = info.dispatcher.as_pycspr_private_key
    cp2: pycspr.types.PublicKey = cp2.as_pycspr_public_key
    session_path: str = paths.get_path_to_contract(info.network, _CONTRACT_FNAME)

    # Set standard deploy parameters.
    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=cp1,
            chain_name=info.network.chain_name
            )

    # Set payment logic.
    payment: ExecutableDeployItem_ModuleBytes = \
        pycspr.create_standard_payment(constants.DEFAULT_TX_FEE)

    # Set session logic.
    session: pycspr.types.ExecutableDeployItem_ModuleBytes = pycspr.types.ExecutableDeployItem_ModuleBytes(
        module_bytes=pycspr.read_wasm(session_path),
        args = [
            pycspr.create_deploy_arg(
                "amount",
                pycspr.cl_value.u512(amount),
                ),
            pycspr.create_deploy_arg(
                "target",
                pycspr.cl_value.storage_key(cp2.account_hash, StorageKeyType.ACCOUNT),
                )
        ]
    )

    return pycspr.create_deploy(params, payment, session)
