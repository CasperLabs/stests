from stests.core.types import CLASSES
from stests.core.types import ENTITIES
from stests.core.types import ENUMS
from stests.core.types import TYPESET
from stests.core.types.utils import Entity



def test_01():
    """Test types are exposed as sets."""
    assert isinstance(CLASSES, set)
    assert isinstance(ENUMS, set)    
    assert isinstance(ENTITIES, set)
    assert isinstance(TYPESET, set)


def test_02():
    """Test classes & enums are in typeset."""
    for i in CLASSES | ENUMS:
        assert i in TYPESET


def test_03():
    """Test instantiation of test class instances."""
    for i in CLASSES:
        assert Entity.instantiate(i) is not None


def test_04():
    """Test codec: encode to dict."""
    for i in [Entity.instantiate(i) for i in CLASSES]:
        assert isinstance(i.to_dict(), dict)


def test_05():
    """Test codec: encode to json."""
    for i in [Entity.instantiate(i) for i in CLASSES]:
        assert isinstance(i.to_json(), str)


def test_06():
    """Test codec: decode from dict."""
    for kls in CLASSES:
        j = Entity.instantiate(kls).to_dict()
        k = kls.from_dict(j)
        assert isinstance(k, kls)


def test_07():
    """Test codec: decode from json."""
    for kls in CLASSES:
        j = Entity.instantiate(kls).to_json()
        k = kls.from_json(j)
        assert isinstance(k, kls)


def test_08():
    """Test entities."""
    for i in ENTITIES:
        assert issubclass(i, Entity)
        assert i in CLASSES
