import dramatiq

from stests.core.types import AccountType



def get_workflow(args):
    """Returns a workflow group that performs various spinup tasks.
    
    """
    from stests.generators.wg_100.phase_01.actors import accounts
    from stests.generators.wg_100.phase_01.actors import contract

    def get_pipeline_for_faucet():
        """Returns a workflow pipeline to initialise a faucet account."""
        return \
            accounts.create.message(args, AccountType.FAUCET) | \
            accounts.fund_faucet.message()


    def get_pipeline_for_contract():
        """Returns a workflow pipeline to initialise a contract account."""
        return \
            accounts.create.message(args, AccountType.CONTRACT) | \
            accounts.fund_contract.message() | \
            contract.deploy.message()


    def get_pipeline_for_user(index):
        """Returns a workflow pipeline to initialise a user account."""
        return \
            accounts.create.message(args, AccountType.USER, index) | \
            accounts.fund_user.message() \


    def get_group_for_users():
        """Returns a workflow group to initialise a set of user accounts."""
        return dramatiq.group(map(
            lambda index: get_pipeline_for_user(index), 
            range(args.user_accounts)
        ))

    # return \
    #     get_pipeline_for_faucet() | \
    #     dramatiq.group([
    #         get_pipeline_for_contract(),
    #         get_group_for_users()
    #         ])
    #     ])

    return dramatiq.group([
        get_pipeline_for_faucet(),
        dramatiq.group([
            get_pipeline_for_contract(),
            get_group_for_users()
            ])
        ])
