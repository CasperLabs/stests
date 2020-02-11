import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import AccountType
from stests.core.domain import RunContext
from stests.core.domain import NodeIdentifier
from stests.core.utils import factory
from stests.core.utils import resources
from stests.generators.wg_100 import constants



# Queue to which message will be dispatched.
_QUEUE = f"{constants.TYPE}.phase_01.setup"


@dramatiq.actor(queue_name=_QUEUE)
def do_reset_cache(ctx: RunContext):   
    """Resets cache in preparation for a new run.
    
    """
    # Flush previous cache data.
    cache.flush_run(ctx)

    # Cache.
    cache.set_run_context(ctx)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: RunContext, index: int, typeof: AccountType):
    """Creates an account for use during the course of the simulation.
    
    """
    # Instantiate.
    account = factory.create_account(index=index, typeof=typeof)

    # Cache.
    cache.set_account(ctx, account)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_faucet(ctx):
    """Funds account to be used as a faucet.
    
    """
    # Set CLX node.
    # TODO: randomize if node index = 0.
    network_id = factory.create_network_identifier("loc1")
    node_id = factory.create_node_identifier(network_id, ctx.node)
    node = cache.get_node(node_id)

    print(node)

    # Set counter-parties.
    validator = node.account
    faucet = cache.get_account()

    # Execute CLX transfer.
    clx.do_transfer(ctx, 100000000, validator, faucet)


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_contract(ctx):
    """Funds contract account (from faucet).
    
    """
    print("TODO: do_fund_contract :: 1. pull accounts.  2. Dispatch transfer.  3. Monitor deploy.")
    return ctx

    # faucet = cache.get_account(ctx.network_id, ctx.cache_namespace, AccountType.FAUCET, 0)
    # clx.do_transfer(
    #     ctx,
    #     10000000,
    #     faucet.key_pair.private_key.as_pem_filepath,
    #     faucet.key_pair.public_key.as_hex,
    #     account.key_pair.public_key.as_hex
    #     )


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_user(ctx, idx):
    """Funds user account (from faucet).
    
    """
    print("TODO: do_fund_user :: 1. pull accounts.  2. Dispatch transfer.  3. Monitor deploy.")
    return ctx

    # faucet = cache.get_account(ctx.network_id, ctx.cache_namespace, AccountType.FAUCET, 0)
    # clx.do_transfer(
    #     ctx,
    #     10000000,
    #     faucet.key_pair.private_key.as_pem_filepath,
    #     faucet.key_pair.public_key.as_hex,
    #     account.key_pair.public_key.as_hex
    #     )


@dramatiq.actor(queue_name=_QUEUE)
def do_deploy_contract(ctx):
    """Deploys smart contract to target network.
    
    """
    print("TODO: do_deploy_contract :: 1. pull account.  2. Dispatch deploy.  3. Monitor deploy.")
    binary_fpath = resources.get_wasm_path(constants.WASM_CONTRACT_FILENAME)
    print(binary_fpath)
    return ctx

    # clx.do_deploy_contract(ctx, account, binary_fpath)