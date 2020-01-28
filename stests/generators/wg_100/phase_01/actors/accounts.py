import casperlabs_client as pyclx
import dramatiq
import time

from stests.core import cache
from stests.core import clx
from stests.core.types.factory import create_account
from stests.core.types import AccountType
from stests.generators.wg_100 import metadata



# Queue to which message will be dispatched.
_QUEUE = f"{metadata.TYPE}.phase_01.accounts"


@dramatiq.actor(queue_name=_QUEUE, actor_name="create_account")
def create(ctx, account_type, account_id=0):
    """Creates an account to be used during simulation execution.
    
    """
    # Instantiate.
    account = create_account(account_type, account_id, ctx.network_id)

    # Cache.
    cache.set_account(ctx.network_id, ctx.cache_namespace, account)

    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def fund_faucet(ctx, account):
    """Funds faucet account (from validator).
    
    """
    clx.do_transfer(
        ctx,
        100000000,
        ctx.args.validator_pvk_pem_fpath,
        ctx.args.validator_pbk_hex,
        account.key_pair.public_key.as_hex
        )
    time.sleep(3)

    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def fund_contract(ctx, account):
    """Funds contract account (from faucet).
    
    """
    faucet = cache.get_account(ctx.network_id, ctx.cache_namespace, AccountType.FAUCET, 0)
    clx.do_transfer(
        ctx,
        10000000,
        faucet.key_pair.private_key.as_pem_filepath,
        faucet.key_pair.public_key.as_hex,
        account.key_pair.public_key.as_hex
        )
    time.sleep(3)

    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def fund_user(ctx, account):
    """Funds user account (from faucet).
    
    """
    faucet = cache.get_account(ctx.network_id, ctx.cache_namespace, AccountType.FAUCET, 0)
    clx.do_transfer(
        ctx,
        10000000,
        faucet.key_pair.private_key.as_pem_filepath,
        faucet.key_pair.public_key.as_hex,
        account.key_pair.public_key.as_hex
        )
    time.sleep(3)

    return ctx, account
