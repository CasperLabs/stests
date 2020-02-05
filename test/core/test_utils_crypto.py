import inspect

from stests.core.utils import crypto


FIXTURES = {
    'KeyEncoding',
    'get_key_pair',
    'get_pbk_pem_from_bytes',
    'get_pvk_pem_from_bytes'
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(crypto)


def test_02():
    """Test slots are exposed."""
    for func in FIXTURES:
        slot = getattr(crypto, func)
        assert inspect.isfunction(slot) or inspect.isclass(slot)


def test_03():
    """Test function: crypto.get_key_pair."""
    for i in crypto.get_key_pair(crypto.KeyEncoding.BYTES):
        assert isinstance(i, bytes)
        assert len(i) == 32

    for i in crypto.get_key_pair(crypto.KeyEncoding.HEX):
        assert isinstance(i, str)
        assert len(i) == 64

    for i in crypto.get_key_pair(crypto.KeyEncoding.PEM):
        assert isinstance(i, bytes)
        assert len(i) in (113, 119)
