import inspect

from stests.core.types import Entity
from stests.core.types import CLASSES
from stests.core.types import ENUMS
from stests.core.types import TYPESET
from stests.core.utils import encoder


FIXTURES = {
    'decode',
    'encode',
    'register_type',
    'TYPESET',
    'TYPEMAP'
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
    """Test all domain types registered in typemap."""
    for i in encoder.TYPEMAP.values():
        assert i in encoder.TYPESET


def test_04():
    """Test all domain types registered in typemap."""
    for i in TYPESET:
        assert(i in encoder.TYPEMAP.values())


def test_05():
    """Test register custom type."""
    class Example():
        pass
    encoder.register_type(Example)
    assert Example in encoder.TYPESET
    assert Example in encoder.TYPEMAP.values()


def test_06():
    """Test all domain classes can be encoded."""
    for i in (Entity.instantiate(i) for i in CLASSES):
        assert isinstance(encoder.encode(i), dict)


def test_07():
    """Test a collection of domain classes can be encoded."""
    for typeof in (tuple, list):
        collection = typeof(Entity.instantiate(i) for i in CLASSES)
        encoded = encoder.encode(collection)
        assert isinstance(encoded, typeof)
        for i in encoded:
            assert isinstance(i, dict)
            assert '_type' in i


def test_08():
    """Test scalar types are not encoded."""
    for scalar in (1, True, 2.0):
        assert encoder.encode(scalar) == scalar


def test_09():
    """Test enum members are converted to strings."""
    for i in ENUMS:
        for j in i:
            assert encoder.encode(j) == str(j)


def test_10():
    """Test round-trip over domain model instances."""
    for i in (Entity.instantiate(i) for i in CLASSES):
        k = encoder.decode(encoder.encode(i))
        assert isinstance(k, type(i))


def test_10():
    """Test round-trip over domain model instance collections."""
    for ctype in (tuple, list):
        c = encoder.decode(encoder.encode(ctype(Entity.instantiate(i) for i in CLASSES)))
        assert isinstance(c, ctype)
