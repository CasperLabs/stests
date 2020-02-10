from stests.core.domain import DCLASS_SET
from stests.core.domain import ENUM_SET
from stests.core.domain import TYPE_SET
from test.core import utils_factory as factory


def test_01():
    """Test types are exposed as sets."""
    assert isinstance(DCLASS_SET, set)
    assert isinstance(ENUM_SET, set)    
    assert isinstance(TYPE_SET, set)


def test_02():
    """Test classes & enums are in typeset."""
    for i in DCLASS_SET | ENUM_SET:
        assert i in TYPE_SET


def test_03():
    """Test instantiation of test class instances."""
    for i in DCLASS_SET:
        assert factory.get_instance(i) is not None


def test_04():
    """Test codec: encode to dict."""
    for i in [factory.get_instance(i) for i in DCLASS_SET]:
        assert isinstance(i.to_dict(), dict)


def test_05():
    """Test codec: encode to json."""
    for i in [factory.get_instance(i) for i in DCLASS_SET]:
        assert isinstance(i.to_json(), str)


def test_06():
    """Test codec: decode from dict."""
    for dcls in DCLASS_SET:
        j = factory.get_instance(dcls).to_dict()
        k = dcls.from_dict(j)
        assert isinstance(k, dcls)


def test_07():
    """Test codec: decode from json."""
    for dcls in DCLASS_SET:
        j = factory.get_instance(dcls).to_json()
        k = dcls.from_json(j)
        assert isinstance(k, dcls)

