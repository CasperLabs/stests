from stests.core.clx.client_factory import get_client
from stests.core.utils.workflow import WorkflowContext
from stests.core.utils import logger


TX_FEE = 10000000
TX_GAS_PRICE = 1


def execute(
    ctx: WorkflowContext,
    amount: int, 
    cp1_pvk_pem_fpath: str,
    cp1_pbk_hex: str,
    cp2_pbk_hex: str
    ):
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Contextual information passed along the flow of execution.
    :param amount: Amount in CLX.motes to be transferred.
    :param cp1_pvk_pem_fpath: Counter party 1 private key PEM file.
    :param cp1_pbk_hex: Counter party 1 public key (hex).
    :param cp2_pbk_hex: Counter party 2 public key (hex).
    :returns: Deploy hash (in hex format).

    """
    pyclx = get_client(ctx)    
    deploy_hash_hex = pyclx.transfer(
        amount=amount,
        private_key=cp1_pvk_pem_fpath,
        from_addr=cp1_pbk_hex,
        target_account_hex=cp2_pbk_hex,
        payment_amount=TX_FEE,
        gas_price=TX_GAS_PRICE
    )

    logger.log(f"PYCLX :: transfer :: {amount} :: {cp1_pbk_hex} :: {cp2_pbk_hex} :: {deploy_hash_hex}")

    return deploy_hash_hex
