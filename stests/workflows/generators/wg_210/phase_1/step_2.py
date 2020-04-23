import typing

import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core import factory
from stests.core.types.chain import ContractType
from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.workflows.generators.utils import constants
from stests.workflows.generators.utils import verification
from stests.workflows.generators.utils.contracts import do_install_contract



# Step label.
LABEL = "set-named-keys"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    # Set contract account.
    account = cache.state.get_account_by_index(ctx, constants.ACC_RUN_CONTRACT)

    # Set contract.
    contract = clx.contracts.get_contract(ContractType.COUNTER_DEFINE_STORED)

    # Set contract keys.
    keys = clx.contracts.get_named_keys(ctx, account, None, contract.NKEYS)

    # Persist keys.
    for key_name, key_hash in keys:
        cache.state.set_named_key(ctx, factory.create_named_key(
            account,
            contract.TYPE,
            key_name,
            key_hash,
        ))


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    # TODO: pull keys and assert
    pass

