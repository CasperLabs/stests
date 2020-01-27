import inspect

from stests.core import clx


FIXTURES = {
    'do_deploy_contract',
    'do_transfer',
    'get_key_pair',
    'KeyEncoding'
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(clx)


def test_02():
    """Test slots are exposed."""
    for func in FIXTURES:
        slot = getattr(clx, func)
        assert inspect.isfunction(slot) or \
               inspect.isclass(slot)


def test_03():
    """Test function: crypto.get_key_pair."""
    for i in clx.get_key_pair(clx.KeyEncoding.BYTES):
        assert isinstance(i, bytes)
        assert len(i) == 32

    for i in clx.get_key_pair(clx.KeyEncoding.HEX):
        assert isinstance(i, str)
        assert len(i) == 64

    for i in clx.get_key_pair(clx.KeyEncoding.PEM):
        assert isinstance(i, bytes)
        assert len(i) in (113, 119)
