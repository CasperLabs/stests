import typing

from stests.core.clx.utils import get_client_from_ctx
from stests.core.clx import utils_defaults as defaults
from stests.core.domain import Account
from stests.core.domain import AccountTransfer
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import logger



def execute(
    ctx: RunContext,
    cp1: Account,
    cp2: Account,
    amount: int,
    is_refundable: bool = True
    ) -> typing.Tuple[Deploy, AccountTransfer]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Contextual information passed along flow of execution.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :param is_refundable: Flag indicating whether a refund is required.
    :returns: Dispatched deploy.

    """
    client = get_client_from_ctx(ctx)
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
        factory.create_deploy(dhash, DeployStatus.DISPATCHED), 
        factory.create_account_transfer(amount, "CLX", cp1, cp2, dhash, is_refundable)
        )
