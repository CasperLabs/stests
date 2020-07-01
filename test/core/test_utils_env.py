import inspect
import os

from stests.core.utils import env


def test_01():
    """Test module is imported."""
    assert inspect.ismodule(env) == True


def test_02():
    """Test functions are exposed."""
    for f in {
        'get_network_id',
        'get_var',
        'get_var_name'
        }:
        assert inspect.isfunction(getattr(env, f)) == True


def test_03():
    """Test function: get_var_name."""
    assert env.get_var_name("test") == "STESTS_TEST"


def test_04():
    """Test function: get_var -> default."""
    assert env.get_var("test_var", 111) == 111


def test_05():
    """Test function: get_var -> custom."""
    os.environ['STESTS_TEST_VAR'] = "TEST-VALUE"
    assert env.get_var("test_var") == "TEST-VALUE"


def test_06():
    """Test function: get_var_name -> custom."""
    os.environ['STESTS_CONFIG_NETWORK_ID'] = "INT-SYS-01"
    assert env.get_network_id() == "INT-SYS-01"
