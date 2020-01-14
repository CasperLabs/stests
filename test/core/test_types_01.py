from stests.core.types import CLASSES
from stests.core.types import ENUMS
from stests.core.types import TYPESET


def test_01():
    """Test types are exposed as sets."""
    assert isinstance(CLASSES, set)
    assert isinstance(ENUMS, set)    
    assert isinstance(TYPESET, set)


def test_02():
    """Test classes & enums are in typeset."""
    for TYPE in CLASSES | ENUMS:
        assert TYPE in TYPESET


def test_03():
    """Test instantiation of test class instances."""
    for TYPE in CLASSES:
        assert TYPE.create() is not None


def test_04():
    """Test codec: encode to dict."""
    for i in [i.create() for i in CLASSES]:
        assert isinstance(i.to_dict(), dict)


def test_05():
    """Test codec: encode to json."""
    for i in [i.create() for i in CLASSES]:
        assert isinstance(i.to_json(), str)


def test_06():
    """Test codec: decode from dict."""
    for kls in CLASSES:
        i = kls.create().to_dict()
        j = kls.from_dict(i)
        assert isinstance(j, kls)


def test_07():
    """Test codec: decode from json."""
    for kls in CLASSES:
        i = kls.create().to_json()
        j = kls.from_json(i)
        assert isinstance(j, kls)
