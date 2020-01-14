import inspect

from stests.core.clx import crypto


FIXTURES = {
    crypto: {
        'create_key_pair', 
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
    """Test function: crypto.create_key_pair."""
    for i in crypto.create_key_pair():
        assert isinstance(i, bytes)
        assert len(i) == 32
