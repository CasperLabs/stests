import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import DeployType
from stests.core.orchestration import ExecutionContext
from stests.core.utils import factory



# Queue to which messages will be dispatched.
_QUEUE = "workflows.generators.contracts"


@dramatiq.actor(queue_name=_QUEUE)
def do_set_contract(
    ctx: ExecutionContext,
    account_index: int,
    contract_type: ContractType
    ):
    """Deploys a contract under a known account.

    :param ctx: Execution context information.
    :param account_index: Index of account to which a contract will be deployed.
    :param contract_type: Type of contract to deploy.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Install contract.
    (node, deploy_hash) = clx.contracts.install_named(ctx, account, contract_type)

    # Update cache.
    deploy = factory.create_deploy_for_run(
        account=account,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.CONTRACT_INSTALL
        )
    cache.state.set_deploy(deploy)
