import typing

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import AccountType
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import constants



# Step label.
LABEL = "create-accounts"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """
    for account_index in range(ctx.args.transfers):
        cache.state.set_account(factory.create_account_for_run(
            ctx,
            index=account_index,
            typeof=AccountType.USER,
        ))


def verify(ctx: ExecutionContext):
    """Step execution verifier.
    
    :param ctx: Execution context information.

    """
    cached = cache.state.get_account_count(ctx)
    expected = ctx.args.transfers
    assert cached == expected, f"cached account total mismatch: actual={cached}, expected={expected}."
