import inspect
import random

from stests.core.types import factory
from stests.core.types.account import Account
from stests.core.types.account import AccountType



def test_01():
    """Test factory module is imported."""
    assert inspect.ismodule(factory) == True



def test_02():
    """Test factory functions are exposed."""
    for f in {
        'create_account',
        }:
        assert inspect.isfunction(getattr(factory, f)) == True


def test_03():
    """Test factory function: create account."""
    i = factory.create_account(
        random.choice(list(AccountType)),
        random.randint(0, 100)
        )
    assert isinstance(i, Account)
