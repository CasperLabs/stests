import random

import pycspr

from pycspr.types import CL_ByteArray
from pycspr.types import CL_Option
from pycspr.types import CL_Type_U64
from pycspr.types import CL_U64
from pycspr.types import CL_U512
from pycspr.types import DeployArgument
from stests.chain import constants
from stests.chain.utils import execute_api
from stests.chain.utils import DeployDispatchInfo
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.events import EventType
from stests.core.utils import paths


# Name of smart contract to dispatch & invoke.
_CONTRACT_FNAME = "transfer_to_account_u512.wasm"

# Maximum value of a transfer ID.
_MAX_TRANSFER_ID = (2 ** 63) - 1


@execute_api("transfer-wasm", EventType.WFLOW_DEPLOY_DISPATCH_FAILURE)
def execute(
    info: DeployDispatchInfo,
    cp2: Account,
    amount: int,
    verbose: bool = True
) -> str:
    """Executes a WASM transfer between 2 counter-parties.

    :param info: Standard information required to dispatch deploy.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param verbose: Flag inidcating whether event will be logged.
    :returns: Dispatched deploy hash.

    """
    # Set counter-parties.
    cp1: pycspr.types.PrivateKey = info.dispatcher.as_pycspr_private_key
    cp2: pycspr.types.PublicKey = cp2.as_pycspr_public_key

    # Set path to WASM.
    session_path: str = paths.get_path_to_contract(info.network, _CONTRACT_FNAME)

    # Set standard deploy parameters.
    params: pycspr.types.DeployParameters = \
        pycspr.create_deploy_parameters(
            account=cp1,
            chain_name=info.network.chain_name
            )


    # Set payment logic.
    payment: pycspr.types.ModuleBytes = \
        pycspr.create_standard_payment(constants.DEFAULT_TX_FEE_WASM_TRANSFER)

    # Set session logic.
    session: pycspr.types.ModuleBytes = \
        pycspr.types.ModuleBytes(
            module_bytes=pycspr.read_wasm(session_path),
            args=[
                DeployArgument(
                    "amount",
                    CL_U512(amount)
                    ),
                DeployArgument(
                    "target",
                    CL_ByteArray(cp2.account_hash)
                    ),
                DeployArgument(
                    "id",
                    CL_Option(CL_U64(random.randint(1, _MAX_TRANSFER_ID)), CL_Type_U64())
                    ),                    
            ]
        )

    # Set deploy.
    deploy = pycspr.create_deploy(params, payment, session)

    # Set deploy approval.
    deploy.approve(cp1)

    # Dispatch.
    info.node.dispatch_deploy(deploy)

    if verbose:
        log_event(
            EventType.WFLOW_DEPLOY_DISPATCHED,
            f"{info.node.address} :: {deploy.hash.hex()} :: transfer (wasm) :: {amount} CSPR :: from {cp1.account_key[:8].hex()} -> {cp2.account_key[:8].hex()} ",
            info.node,
            deploy_hash=deploy.hash,
            )

    return deploy.hash.hex()
