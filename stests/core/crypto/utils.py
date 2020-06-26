import base64



def get_bytes_from_pem_file(fpath: str) -> bytes:
    """Returns bytes from a pem file.
    
    """
    with open(fpath, 'r') as fstream:
        as_pem = fstream.readlines()
    as_b64 = [l for l in as_pem if l and not l.startswith("-----")][0].strip()
    as_bytes = base64.b64decode(as_b64)

    return len(as_bytes) % 32 == 0 and as_bytes[:32] or as_bytes[-32:]
