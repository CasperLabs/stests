import inspect

from stests.core import domain
from stests.core.utils import encoder
from test.core import utils_factory as factory





FIXTURES = {
    'decode',
    'encode',
    'register_type',
    'ENUM_TYPE_SET',
    'ENUM_VALUE_MAP',
    'DCLASS_MAP',
    'DCLASS_SET',
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(encoder)


def test_02():
    """Test slots are exposed."""
    for func in FIXTURES:
        slot = getattr(encoder, func)
        assert inspect.isfunction(slot) or isinstance(slot, (dict, set))


def test_03():
    """Test all data class types are registered in data class map."""
    for i in encoder.DCLASS_MAP.values():
        assert i in encoder.DCLASS_SET


def test_04():
    """Test all data class map entries are in data class set."""
    for i in encoder.DCLASS_SET:
        assert(i in encoder.DCLASS_MAP.values())


def test_05():
    """Test register custom type."""
    class Example():
        pass
    encoder.register_type(Example)
    assert Example in encoder.DCLASS_SET
    assert Example in encoder.DCLASS_MAP.values()


def test_06():
    """Test all domain data classes can be encoded."""
    for i in (_get_test_dclass_instances()):
        assert isinstance(encoder.encode(i), dict)


def test_07():
    """Test a collection of domain classes can be encoded."""
    for typeof in (tuple, list):
        collection = typeof(_get_test_dclass_instances())
        encoded = encoder.encode(collection)
        assert isinstance(encoded, typeof)
        for i in encoded:
            assert isinstance(i, dict)
            assert '_type_key' in i
            assert '_ts_created' in i
            assert '_uid' in i


def test_08():
    """Test scalar types are not encoded."""
    for scalar in (1, True, 2.0):
        assert encoder.encode(scalar) == scalar


def test_09():
    """Test enum members are converted to strings."""
    for i in domain.ENUM_SET:
        for j in i:
            assert encoder.encode(j) == j.name


def test_10():
    """Test round-trip over domain model instances."""
    for i in _get_test_dclass_instances():
        k = encoder.decode(encoder.encode(i))
        assert isinstance(k, type(i))


def test_10():
    """Test round-trip over domain model instance collections."""
    for ctype in (tuple, list):
        c = encoder.decode(encoder.encode(ctype(_get_test_dclass_instances())))
        assert isinstance(c, ctype)


def _get_test_dclass_instances():
    return (factory.get_instance(i) for i in domain.DCLASS_SET)