import dataclasses
import enum

from stests.core.types import TYPE_SET
from stests.core.utils import encoder
from test.core import utils_factory as factory





def test_01():
    """Test types are exposed as a set."""
    assert isinstance(TYPE_SET, set)


def test_02():
    """Test classes & enums are in typeset."""
    for i in [i for i in TYPE_SET if not issubclass(i, enum.Enum)]:
        assert factory.get_instance(i) is not None


# def test_03():
#     """Test instantiation of test class instances."""
#     for i in DCLASS_SET:
#         assert factory.get_instance(i) is not None


# def test_04():
#     """Test codec: encode to dict."""
#     for i in [factory.get_instance(i) for i in DCLASS_SET]:
#         assert isinstance(encoder.as_dict(i), dict)


# def test_05():
#     """Test codec: encode to json."""
#     for i in [factory.get_instance(i) for i in DCLASS_SET]:
#         assert isinstance(encoder.as_json(i), bytes)


# def test_06():
#     """Test codec: decode from dict."""
#     for dcls in DCLASS_SET:
#         i = factory.get_instance(dcls)
#         j = encoder.as_dict(i)
#         k = encoder.from_dict(j)
#         assert isinstance(k, dcls)


# def test_07():
#     """Test codec: decode from json."""
#     for dcls in DCLASS_SET:
#         i = factory.get_instance(dcls)
#         j = encoder.as_json(i)
#         k = encoder.from_json(j)
#         assert isinstance(k, dcls)

