from stests.core.clx.utils import get_client_from_ctx
from stests.core.domain import Account
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import Node
from stests.core.domain import RunContext
from stests.core.utils import factory
from stests.core.utils import logger


# Default transaction fee to apply.
TX_FEE = 10000000

# Default gas price to apply.
TX_GAS_PRICE = 1


def execute(ctx: RunContext, cp1: Account, cp2: Account, amount: int) -> Deploy:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Contextual information passed along flow of execution.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :returns: Dispatched deploy.

    """
    client = get_client_from_ctx(ctx)
    deploy_hash = client.transfer(
        amount=amount,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_as_pem_filepath,
        target_account_hex=cp2.public_key,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=TX_FEE,
        gas_price=TX_GAS_PRICE
    )

    logger.log(f"PYCLX :: transfer :: {amount} :: {cp1.public_key[:8]} -> {cp2.public_key[:8]} :: {deploy_hash}")

    return factory.create_deploy(deploy_hash, DeployStatus.DISPATCHED)
