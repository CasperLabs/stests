from stests.core.clx.client_factory import get_client
from stests.core.domain import Account
from stests.core.domain import Deploy
from stests.core.domain import RunContext
from stests.core.utils import logger


TX_FEE = 10000000
TX_GAS_PRICE = 1


def execute(ctx: RunContext, cp1: Account, cp2: Account, amount: int) -> Deploy:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Generator execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.
    :returns: Dispatched deploy.

    """
    pyclx = get_client(ctx)    
    deploy_hash_hex = pyclx.transfer(
        amount=amount,
        from_addr=cp1.public_key,
        private_key=cp1.private_key_pem_path,
        target_account_hex=cp2.public_key,
        # TODO: allow these to be passed in
        payment_amount=TX_FEE,
        gas_price=TX_GAS_PRICE
    )

    logger.log(f"PYCLX :: transfer :: {amount} :: {cp1.public_key[:8]} -> {cp1.public_key[:8]} :: {deploy_hash_hex}")

    return deploy_hash_hex
