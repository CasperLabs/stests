import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.types.chain import ContractType
from stests.core.types.chain import DeployType
from stests.core.types.orchestration import ExecutionContext
from stests.core import factory



# Queue to which messages will be dispatched.
_QUEUE = "workflows.generators.contracts"


@dramatiq.actor(queue_name=_QUEUE)
def do_install_contract(ctx: ExecutionContext, account_index: int, contract_type: ContractType):
    """Installs a contract for subsequent invocation by hash.

    :param ctx: Execution context information.
    :param account_index: Index of account under which contract will be installed.
    :param contract_type: Type of contract to be installed.
    
    """
    # Set account.
    account = cache.state.get_account_by_index(ctx, account_index)

    # Set contract.
    contract = clx.contracts.get_contract(contract_type)

    # Install contract.
    node, deploy_hash, keys = contract.install(ctx, account)

    # Persist deploy.
    deploy = factory.create_deploy_for_run(
        account=account,
        ctx=ctx, 
        node=node, 
        deploy_hash=deploy_hash, 
        typeof=DeployType.CONTRACT_INSTALL
        )
    cache.state.set_deploy(deploy)

    # Persist named keys.
    for key_name, key_hash in keys:
        key = factory.create_account_named_key(
            account,
            contract.TYPE,
            key_name,
            network.name,
            key_hash,
        )
        cache.state.set_account_named_key(ctx, key)
