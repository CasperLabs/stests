import inspect

from stests.core.clx import crypto


FIXTURES = {
    crypto: {
        'get_account_keys', 
        'get_key_pair'
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
    """Test function: crypto.get_account_keys."""
    keys = crypto.get_account_keys()
    assert isinstance(keys, tuple)
    assert len(keys) == 2
    for i in keys:
        assert isinstance(i, tuple)
        assert len(i) == 3
        assert isinstance(i[0], bytes)
        assert isinstance(i[1], str)
        assert isinstance(i[2], bytes)
        assert len(i[0]) == 32
        assert len(i[1]) == 64
        assert len(i[2]) in (113, 119)


def test_04():
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
