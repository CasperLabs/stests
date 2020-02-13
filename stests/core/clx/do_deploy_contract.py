from stests.core.clx.utils import get_client
from stests.core.clx import utils_defaults as defaults
from stests.core.domain import Account
from stests.core.domain import RunContext
from stests.core.utils import logger



def execute(
    ctx: RunContext,
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

    logger.log(f"TODO :: deploy-contract :: {account.key_pair.public_key.as_hex} :: {wasm_filepath}")

    return "TODO: dispatch contract deploy"


