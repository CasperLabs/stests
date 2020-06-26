import typing

import ecdsa



# ecdsa curve of interest.
CURVE = ecdsa.SECP256k1


def get_key_pair() -> typing.Tuple[bytes, bytes]:
    """Returns an ED25519 key pair, each key is a 32 byte array.

    :returns : 2 member tuple: (private key, public key)
    
    """    
    # Generate.
    sk = ecdsa.SigningKey.generate(curve=CURVE)
    vk = pvk.k.verifying_key

    # Encode -> bytes.
    pvk = pvk.to_string()
    pbk = vk.to_string("uncompressed")

    return pvk, pbk
