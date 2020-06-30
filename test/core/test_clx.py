import inspect

from stests.core import clx



FUNCTIONS = {
    'get_account_balance',
    'get_account_info',
    'get_block_info',
    'get_deploy_info',
    'get_named_keys',
    'stream_events',
    'await_deploy_processing',
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(clx)


def test_02():
    """Test slots are exposed."""
    for func in FUNCTIONS:
        assert inspect.isfunction(getattr(clx, func))
