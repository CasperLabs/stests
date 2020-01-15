import dramatiq

from stests.core.types import AccountType



def get_workflow(ctx, args):
    """Returns a workflow group that performs various spinup tasks.
    
    """
    # Import actors JIT so as to ensure that broker has been injected.
    from stests.generators.wg_100.phase_01.actors import accounts
    from stests.generators.wg_100.phase_01.actors import contracts

    def get_pipeline_for_contract():
        """Returns a workflow pipeline to initialise a contract account."""
        return \
            accounts.create.message(ctx, AccountType.CONTRACT, 0) | \
            contracts.deploy.message()


    def get_pipeline_for_user(index):
        """Returns a workflow pipeline to initialise a user account."""
        return \
            accounts.create.message(ctx, AccountType.USER, index)


    def get_group_for_users():
        """Returns a workflow group to initialise a set of user accounts."""
        return dramatiq.group(map(
            lambda index: get_pipeline_for_user(index), 
            range(args.max_user_accounts)
        ))


    return dramatiq.group([
        get_pipeline_for_contract(),
        get_group_for_users()
        ])
