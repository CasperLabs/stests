import typing

from google.protobuf.json_format import MessageToDict



def parse_deploy_info(deploy_info) -> dict:
    """Parses deploy info returned from chain.
    
    """
    if deploy_info is None:
        return dict()

    return _parse_dict(MessageToDict(deploy_info))


def _parse_dict(obj: typing.Any) -> typing.Any:
    """Performs a parse over a dictionary deserialized from protobuf layer.
    
    """
    if isinstance(obj, dict):        
        return {k: _parse_dict(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_parse_dict(i) for i in obj]

    try:
        return int(obj)
    except:
        pass

    # TODO: convert keys + sigs to hex

    return obj        