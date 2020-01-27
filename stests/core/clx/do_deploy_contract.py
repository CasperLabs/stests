from stests.core.clx.client_factory import get_client
from stests.core.types import Account
from stests.core.utils.workflow import WorkflowContext
from stests.core.utils import logger


TX_FEE = 10000000
TX_GAS_PRICE = 1


def execute(
    ctx: WorkflowContext,
    account: Account,
    wasm_filepath: str
    ):
    """Deploys a smart contract to chain.

    :param ctx: Contextual information passed along the flow of execution.
    :param account: Account to be associated with contract.
    :param wasm_filepath: Path to smart contract's wasm file.
    :returns: Deploy hash (in hex format).

    """
    pyclx = get_client(ctx)    

    deploy_hash_hex = "TODO: dispatch contract deploy"

    logger.log(f"PYCLX :: deploy-contract :: {account.key_pair.public_key.as_hex} :: {wasm_filepath} :: {deploy_hash_hex}")

    return deploy_hash_hex


