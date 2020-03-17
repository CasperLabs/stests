import typing

from casperlabs_client.abi import ABI

from stests.core.clx import defaults
from stests.core.clx import utils
from stests.core.clx.utils import get_client
from stests.core.clx.utils import get_client_contract_hash
from stests.core.clx.utils import get_client_contract_path
from stests.core.clx.utils import clx_op
from stests.core.clx.query import get_balance
from stests.core.domain import Account
from stests.core.domain import ClientContractType
from stests.core.domain import Network
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import DeployType
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger



@clx_op
def do_refund(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int = None
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a refund between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be refunded.

    :returns: Dispatched deploy.

    """
    assert cp1 is not None
    assert cp2 is not None

    amount = amount or (get_balance(ctx, cp1) - defaults.CLX_TX_FEE)
    if amount <= 0:
        logger.log_warning("Counter party 1 does not have enough CLX to pay refund transaction fee.")
        return

    return do_transfer(ctx, cp1, cp2, amount, False, DeployType.REFUND)


@clx_op
def do_transfer(
    ctx: ExecutionContext,
    cp1: Account,
    cp2: Account,
    amount: int,
    is_refundable: bool = True,
    deploy_type: DeployType = DeployType.TRANSFER
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param is_refundable: Flag indicating whether a refund is required.

    :returns: Dispatched deploy & transfer.

    """
    node, client  = get_client(ctx)
    dhash = client.transfer(
        amount=amount,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_as_pem_filepath,
        target_account_hex=cp2.public_key,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    logger.log(f"PYCLX :: transfer :: {amount} CLX :: {cp1.public_key[:8]} -> {cp2.public_key[:8]} :: {dhash}")

    return (
        factory.create_deploy_for_run(ctx, node, dhash, deploy_type), 
        factory.create_transfer(ctx, amount, "CLX", cp1, cp2, dhash, is_refundable)
        )


@clx_op
def do_deploy_client_contract(network: Network, contract_type: ClientContractType, contract_name: str) -> str:
    """Deploys a client side smart contract to chain for future reference.

    :param network: Network to which a client contract is being deployed.
    :param contract_type: Type of contract to be deployed.
    :param contract_name: Name of contract as specified in wasm blob.

    :returns: Contract hash (in hex format).

    """
    # Set client.
    _, client = utils.get_client(network)

    # Dispatch deploy.
    session=utils.get_client_contract_path(contract_type)
    session_args = ABI.args([
        ABI.string_value("target", "hash")
        ])
    dhash = client.deploy(
        session=session,
        session_args=session_args,
        from_addr=network.faucet.public_key,
        private_key=network.faucet.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    # Get block hash.
    dinfo = client.showDeploy(dhash, wait_for_processed=True)
    bhash = dinfo.processing_results[0].block_info.summary.block_hash.hex()

    # Get contract hash.
    chash = utils.get_client_contract_hash(client, network.faucet, bhash, contract_name)

    return chash
