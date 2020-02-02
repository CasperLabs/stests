import casperlabs_client as pyclx
import dramatiq
import time

from stests.core import cache
from stests.core import clx
from stests.core.types import Account
from stests.core.types import AccountType
from stests.generators.wg_100 import metadata


# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.accounts"



@dramatiq.actor(queue_name=_QUEUE)
def do_create_faucet_account(ctx):
    # Instantiate.
    account = Account(typeof=AccountType.FAUCET)

    # Cache.
    cache.set_account(ctx.generator_id, account)

    # Pass to next actor in pipeline.
    # TODO: optimise pipeline in order to reduce cache hits
    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def do_create_contract_account(ctx):
    # Instantiate.
    account = Account(typeof=AccountType.CONTRACT)

    # Cache.
    cache.set_account(ctx.generator_id, account)

    # Pass to next actor in pipeline.
    # TODO: optimise pipeline in order to reduce cache hits
    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def do_create_user_account(ctx, idx):
    # Instantiate.
    account = Account(idx=idx, typeof=AccountType.USER)

    # Cache.
    cache.set_account(ctx.generator_id, account)

    # Pass to next actor in pipeline.
    # TODO: optimise pipeline in order to reduce cache hits
    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def do_fund_faucet(ctx):
    """Funds faucet account (from validator).
    
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
