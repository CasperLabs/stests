import dramatiq

from stests.core.types import AccountType
from stests.generators.wg_100.phase_01.actors import accounts
from stests.generators.wg_100.phase_01.actors import contract



def execute(ctx):
    """Returns a workflow group that performs various spinup tasks.
    
    """
    # return \
    #     get_pipeline_for_faucet() | \
    #     dramatiq.group([
    #         get_pipeline_for_contract(),
    #         get_group_for_users()
    #         ])
    #     ])

    # return dramatiq.group([
    #     _get_pipeline_for_faucet(ctx),
    #     dramatiq.group([
    #         _get_pipeline_for_contract(ctx),
    #         _get_group_for_users(ctx)
    #         ])
    #     ])
    workflow = accounts.get_group_for_account_creation(ctx)
    workflow.run()


def _get_group_for_account_creation(ctx):
    """Returns a workflow pipeline to initialise a faucet account.
    
    """
    return dramatiq.group([
        accounts.create.message(ctx, AccountType.FAUCET),
        accounts.create.message(ctx, AccountType.CONTRACT),
        dramatiq.group(map(
                lambda index: accounts.create.message(ctx, AccountType.USER, index), 
                range(1, ctx.user_accounts + 1)
            ))        
        ])


def _get_pipeline_for_faucet(ctx):
    """Returns a workflow pipeline to initialise a faucet account.
    
    """
    return \
        accounts.create.message(ctx, AccountType.FAUCET) | \
        accounts.fund_faucet.message()


def _get_pipeline_for_contract(ctx):
    """Returns a workflow pipeline to initialise a contract account.
    
    """
    return \
        accounts.create.message(ctx, AccountType.CONTRACT) | \
        accounts.fund_contract.message() | \
        contract.deploy.message()


def _get_pipeline_for_user(ctx, index):
    """Returns a workflow pipeline to initialise a user account.
    
    """
    return \
        accounts.create.message(ctx, AccountType.USER, index) | \
        accounts.fund_user.message() \


def _get_group_for_users(ctx):
    """Returns a workflow group to initialise a set of user accounts.
    
    """
    return dramatiq.group(map(
        lambda index: _get_pipeline_for_user(ctx, index), 
        range(1, ctx.user_accounts + 1)
    ))
