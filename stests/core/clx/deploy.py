import typing

from stests.core.clx import defaults
from stests.core.clx.utils import get_client
from stests.core.clx.utils import get_client
from stests.core.domain import Account
from stests.core.domain import Transfer
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import DeployType
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import logger



def do_transfer(
    ctx: RunContext,
    cp1: Account,
    cp2: Account,
    amount: int,
    is_refundable: bool = True
    ) -> typing.Tuple[Deploy, Transfer]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Generator run contextual information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param is_refundable: Flag indicating whether a refund is required.

    :returns: Dispatched deploy.

    """
    node, client  = get_client(ctx)
    deploy_hash = client.transfer(
        amount=amount,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_as_pem_filepath,
        target_account_hex=cp2.public_key,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    logger.log(f"PYCLX :: transfer :: {amount} CLX :: {cp1.public_key[:8]} -> {cp2.public_key[:8]} :: {deploy_hash}")

    return (
        factory.create_deploy_for_run(ctx, node, deploy_hash, DeployType.TRANSFER), 
        factory.create_transfer(ctx, amount, "CLX", cp1, cp2, deploy_hash, is_refundable)
        )


def do_deploy_contract(ctx: RunContext, account: Account, wasm_filepath: str):
    """Deploys a smart contract to chain.

    :param ctx: Generator run contextual information.
    :param account: Account to be associated with contract.
    :param wasm_filepath: Path to smart contract's wasm file.

    :returns: Deploy hash (in hex format).

    """
    _, client = get_client(ctx)

    logger.log(f"TODO :: deploy-contract :: {account.key_pair.public_key.as_hex} :: {wasm_filepath}")

    return "TODO: dispatch contract deploy"
