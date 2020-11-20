from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.orchestration import ExecutionContext



# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    cache.state.set_account(factory.create_account_for_run(
        ctx,
        index=1,
        typeof=AccountType.USER,
    ))


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    cached = cache.state.get_account_count(ctx)
    assert cached == 1, f"cached account total mismatch: actual={cached}, expected={1}."
