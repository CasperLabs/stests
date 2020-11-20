import inspect

from stests.core.types import TYPE_SET
from stests.core.utils import encoder
from test.core import utils_factory as factory



FIXTURES = {
    'as_dict',
    'as_json',
    'from_dict',
    'from_json',
    'decode',
    'encode',
    'register_type',
    'initialise',
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
    """Test all data classes can be encoded."""
    for i in (_get_test_dclass_instances()):
        assert isinstance(encoder.encode(i), dict)


def test_06():
    """Test a collection of classes can be encoded."""
    for typeof in (tuple, list):
        collection = typeof(_get_test_dclass_instances())
        encoded = encoder.encode(collection)
        assert isinstance(encoded, typeof)
        for i in encoded:
            assert isinstance(i, dict)
            assert '_type_key' in i


def test_07():
    """Test scalar types are encoded as is."""
    for scalar in (1, True, 2.0):
        assert encoder.encode(scalar) == scalar


def test_08():
    """Test enum members are converted to strings."""
    for i in encoder.ENUM_TYPE_SET:
        for j in i:
            assert encoder.encode(j) == j.name


def test_09():
    """Test round-trip over instances."""
    for i in _get_test_dclass_instances():
        k = encoder.decode(encoder.encode(i))
        assert isinstance(k, type(i))


def test_10():
    """Test round-trip over collections."""
    for ctype in (tuple, list):
        c = encoder.decode(encoder.encode(ctype(_get_test_dclass_instances())))
        assert isinstance(c, ctype)


def test_11():
    """Test initialisation."""
    assert encoder.IS_INITIALISED == False
    encoder.initialise()
    assert encoder.IS_INITIALISED


def test_11():
    """Test registration of non core types."""
    encoder.initialise()
    from stests.generators.meta import GENERATOR_SET
    for generator in GENERATOR_SET:
        for i in generator.TYPE_SET:
            assert i in encoder.DCLASS_SET


def test_12():
    """Test register custom type."""
    class Example():
        pass
    encoder.register_type(Example)
    assert Example in encoder.DCLASS_SET
    assert Example in encoder.DCLASS_MAP.values()


def _get_test_dclass_instances():
    return [factory.get_instance(i) for i in encoder.DCLASS_SET]