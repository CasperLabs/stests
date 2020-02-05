import time

import casperlabs_client as pyclx
import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.types import Account
from stests.core.types import AccountType
from stests.core.types import GeneratorRun
from stests.core.types import AccountIdentifier

from stests.core.utils import resources
from stests.generators.wg_100 import constants



# Queue to which message will be dispatched.
_QUEUE = f"{constants.TYPE}.phase_01.setup"


@dramatiq.actor(queue_name=_QUEUE)
def do_reset_cache(ctx: GeneratorRun):   
    """Resets cache in preparation for a new run.
    
    """
    # Flush previous cache data.
    cache.flush_run(ctx)

    # Cache.
    cache.set_run(ctx)

    print(cache.get_network(ctx.get_network_identifier()))
    print(cache.get_node(ctx.get_node_identifier()))

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_create_account(ctx: GeneratorRun, index: int, typeof: AccountType):
    """Creates an account for use during the course of the simulation.
    
    """
    # Instantiate.
    account = Account.create(
        index=index,
        generator=ctx.get_run_identifier(),
        network=ctx.get_network_identifier(),
        typeof=typeof
        )

    # Cache.
    cache.set_account(account)

    # Chain.
    return ctx


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_faucet(ctx):
    """Funds account to be used as a faucet.
    
    """
    print("TODO: do_fund_faucet :: 1. pull accounts.  2. Dispatch transfer.  3. Monitor deploy.")
    return ctx

    # clx.do_transfer(
    #     ctx,
    #     100000000,
    #     ctx.validator_pvk_pem_fpath,
    #     ctx.validator_pbk_hex,
    #     account.key_pair.public_key.as_hex
    #     )



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