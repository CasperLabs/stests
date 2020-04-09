import base64
import typing

from google.protobuf.json_format import MessageToDict



def parse_block_info(block_info) -> dict:
    """Parses block info returned from chain over grpc channel.
    
    """
    if block_info is None:
        return dict()

    return _parse_dict(MessageToDict(block_info))


def parse_deploy_info(deploy_info) -> dict:
    """Parses deploy info returned from chain over grpc channel.
    
    """
    if deploy_info is None:
        return dict()

    return _parse_dict(MessageToDict(deploy_info))


def _parse_dict(obj: typing.Any, key=None) -> typing.Any:
    """Performs a parse over a dictionary deserialized from protobuf layer.
    
    """
    if isinstance(obj, dict):        
        return {k: _parse_dict(v, k) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_parse_dict(i, key) for i in obj]

    try:
        return int(obj)
    except:
        pass
    
    try:
        if 'Hash' in key or 'Key' in key or key.startswith('sig'):
            return base64.b64decode(obj).hex()
    except:
        pass

    return obj        
