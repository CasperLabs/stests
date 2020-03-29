import typing

from casperlabs_client.abi import ABI

from stests.core.clx import defaults
from stests.core.clx import utils
from stests.core.clx.query import get_balance
from stests.core.domain import *
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory
from stests.core.utils import logger



def do_deploy_contract_to_name(
    ctx: ExecutionContext,
    account: Account,
    contract_type: ContractType
    ) -> typing.Tuple[Node, str]:
    """Deploys a smart contract to a known name for future use.

    :param ctx: Execution context information.
    :param account: Account under which contract will be deployed.
    :param contract_type: Type of contract to be deployed.

    :returns: 2 member tuple -> (node, deploy hash)

    """
    # Set client.
    node, client = utils.get_client(ctx)

    # Set args.
    session=utils.get_contract_path(ContractType[contract_type])
    
    # Dispatch.
    dhash = client.deploy(
        session=session,
        from_addr=account.public_key,
        private_key=account.private_key_as_pem_filepath,
        # TODO: allow these to be passed in via standard arguments
        payment_amount=defaults.CLX_TX_FEE,
        gas_price=defaults.CLX_TX_GAS_PRICE
    )
    logger.log(f"PYCLX :: deploy-contract :: {contract_type} :: deploy-hash={dhash}")

    return (node, dhash)
