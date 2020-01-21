import inspect

from stests.core.clx import crypto



FIXTURES = {
    crypto: {
        'get_key_pair',
        }
}


def test_01():
    """Test modules are imported."""
    for mod in FIXTURES.keys():
        assert inspect.ismodule(mod) == True


def test_02():
    """Test functions are exposed."""
    for mod, funcs in FIXTURES.items():
        for func in funcs:
            assert inspect.isfunction(getattr(mod, func)) == True


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
