import inspect

from stests.core import clx



FUNCTIONS = {
    'do_deploy_contract',
    'do_deploy_network_contract',
    'do_refund',
    'do_transfer',
    'get_balance',
    'get_block',
    'get_client',
    'get_contract_hash',
    'get_deploys',
    'stream_events',
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(clx)


def test_02():
    """Test slots are exposed."""
    for func in FUNCTIONS:
        assert inspect.isfunction(getattr(clx, func))

