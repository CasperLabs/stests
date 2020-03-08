import typing

from stests.core.clx import defaults
from stests.core.clx.utils import get_client
from stests.core.clx.utils import clx_op
from stests.core.clx.query import get_balance
from stests.core.domain import Account
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import DeployType
from stests.core.orchestration import ExecutionRunInfo
from stests.core.utils import factory
from stests.core.utils import logger



@clx_op
def do_refund(
    ctx: ExecutionRunInfo,
    cp1: Account,
    cp2: Account,
    amount: int = None
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a refund between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Generator run contextual information.
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
    ctx: ExecutionRunInfo,
    cp1: Account,
    cp2: Account,
    amount: int,
    is_refundable: bool = True,
    deploy_type: DeployType = DeployType.TRANSFER
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Generator run contextual information.
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
def do_deploy_contract(ctx: ExecutionRunInfo, account: Account, wasm_filepath: str):
    """Deploys a smart contract to chain.

    :param ctx: Generator run contextual information.
    :param account: Account to be associated with contract.
    :param wasm_filepath: Path to smart contract's wasm file.

    :returns: Deploy hash (in hex format).

    """
    _, client = get_client(ctx)

    logger.log(f"PYCLX :: deploy-contract :: {account.key_pair.public_key.as_hex} :: {wasm_filepath}")

    return "TODO: dispatch contract deploy"
