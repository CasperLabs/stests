import inspect
import os
import pathlib

import pytest

from stests.core import crypto



FIXTURES = {
    'HashAlgorithm',
    'HashEncoding',
    'KeyAlgorithm',
    'KeyEncoding',
    'get_account_key',
    'get_hash',
    'get_key_pair',
    'get_key_pair_from_pvk_pem_file',
    'get_pvk_pem_file_from_bytes',
}


def test_01():
    """Test module import."""
    assert inspect.ismodule(crypto)
    for func in FIXTURES:
        slot = getattr(crypto, func)
        assert inspect.isfunction(slot) or inspect.isclass(slot)


def _test_02_parameterizations():
    """Test parameterizations."""   
    for algo, encoding, expected_type, expected_pvk_len, expected_pbk_len in (
        (crypto.KeyAlgorithm.ED25519, crypto.KeyEncoding.BYTES, bytes, 32, 32),
        (crypto.KeyAlgorithm.ED25519, crypto.KeyEncoding.HEX, str, 64, 64),
        (crypto.KeyAlgorithm.SECP256K1, crypto.KeyEncoding.BYTES, bytes, 32, 65),
        (crypto.KeyAlgorithm.SECP256K1, crypto.KeyEncoding.HEX, str, 64, 130),
        ):
        yield algo, encoding, expected_type, expected_pvk_len, expected_pbk_len


@pytest.mark.parametrize("algo, encoding, expected_type, expected_pvk_len, expected_pbk_len", _test_02_parameterizations())
def test_02(algo, encoding, expected_type, expected_pvk_len, expected_pbk_len):
    """Test function: crypto.get_key_pair."""
    pvk, pbk = crypto.get_key_pair(algo, encoding)
    assert isinstance(pvk, expected_type)
    assert isinstance(pbk, expected_type)
    assert len(pvk) == expected_pvk_len
    assert len(pbk) == expected_pbk_len


@pytest.mark.parametrize("algo", list(crypto.KeyAlgorithm))
def test_03(algo):
    """Test function: crypto.get_pvk_pem_file_from_bytes."""
    encoding = crypto.KeyEncoding.BYTES
    pvk, pbk = crypto.get_key_pair(algo, encoding)    

    fpath = crypto.get_pvk_pem_file_from_bytes(pvk, algo)
    assert pathlib.Path(fpath).exists()

    pvk1, pbk1 = crypto.get_key_pair_from_pvk_pem_file(fpath, algo, encoding)
    assert pvk == pvk1
    assert pbk == pbk1


@pytest.mark.parametrize("algo", list(crypto.KeyAlgorithm))
def test_04(algo):
    """Test function: crypto.get_account_key."""
    _, pbk = crypto.get_key_pair(algo, crypto.KeyEncoding.HEX)
    account_key = crypto.get_account_key(algo, pbk)
    assert isinstance(account_key, str)
    assert len(account_key) == 64
