import typing

from stests.core.clx import defaults
from stests.core.clx import utils
from stests.core.domain import Account
from stests.core.domain import ContractType
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger



# Type of contract.
TYPE = ContractType.COUNTER_DEFINE_STORED

# Wasm file name.
WASM = "counter_define_stored.wasm"

# Name of contract - see use when passed as session-name.
NAME = "counter"

# Flag indicating whether this contract can be installed under a single account and invoked by other accounts.
IS_SINGLETON = False


def increment(ctx: ExecutionContext, account: Account) -> typing.Tuple[Node, str]:
    """Increments counter previously installed under an account.
    
    """
    # Set client.
    node, client  = utils.get_client(ctx)

    # Set contract.
    contract = cache.infra.get_contract(ctx, TYPE)    
    if contract is None:
        raise ValueError(f"{WASM} has not been installed upon chain.  Execute stests-set-contract {ctx.network}.")

    # Dispatch deploy.
    deploy_hash = client.deploy(
        session_hash=counter_inc_address,
        session_args=[ABI.key_hash("counter_key", contract.hash)],
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: review how these are being assigned
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )

    logger.log(f"PYCLX :: deploy dispatched :: {deploy_hash} :: COUNTER_DEFINE.increment :: address={account.public_key}")

    return (node, deploy_hash)