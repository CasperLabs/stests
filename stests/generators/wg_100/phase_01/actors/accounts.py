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


@dramatiq.actor(queue_name=_QUEUE, actor_name="create_account")
def create(ctx, typeof, idx=1):
    """Creates an account to be used during simulation execution.

    :param ctx: Generator context information.
    :param typeof: Type of account to generate.
    :param idx: Run specific account index.
    
    """
    # Instantiate.
    account = Account(idx=idx, typeof=typeof)

    # Cache.
    cache.set_account(ctx.generator_id, account)

    # Pass to next actor in pipeline.
    return ctx, account


def get_group_for_account_creation(ctx):
    """Returns a workflow pipeline to initialise a faucet account.
    
    """
    return dramatiq.group([
        create.message(ctx, AccountType.FAUCET),
        create.message(ctx, AccountType.CONTRACT),
        dramatiq.group(map(
                lambda index: create.message(ctx, AccountType.USER, index), 
                range(1, ctx.user_accounts + 1)
            ))        
        ])


@dramatiq.actor(queue_name=_QUEUE)
def fund_faucet(ctx, account):
    """Funds faucet account (from validator).
    
    """
    return ctx, account

    clx.do_transfer(
        ctx,
        100000000,
        ctx.validator_pvk_pem_fpath,
        ctx.validator_pbk_hex,
        account.key_pair.public_key.as_hex
        )
    time.sleep(3)

    return ctx, account


@dramatiq.actor(queue_name=_QUEUE)
def fund_contract(ctx, account):
    """Funds contract account (from faucet).
    
    """
    return ctx, account

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
    return ctx, account

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
