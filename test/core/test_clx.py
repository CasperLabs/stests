import inspect

from stests.core import clx


FIXTURES = {
    'do_deploy_contract',
    'do_transfer',
    'get_balance',
    'get_block',
    'get_deploys',
    'stream_events',
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(clx)


def test_02():
    """Test slots are exposed."""
    for func in FIXTURES:
        assert inspect.isfunction(getattr(clx, func))

