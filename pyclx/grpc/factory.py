import typing

import grpc

from pyclx.grpc.service import GRPCService
from pyclx.grpc.pb2.casper_pb2_grpc import CasperServiceStub
from pyclx.grpc.pb2.control_pb2_grpc import ControlServiceStub



def get_casper_service(
    host: str,
    port: int,
    node_id: str = None,
    certificate_file: str = None
    ) -> GRPCService:
    """Returns a casper service manager.

    :param host: Service host identifier.
    :param port: Port over which service is reachable.
    :param node_id: Node identifier.
    :param certificate_file: Node certificate file used to establish secure handshake.
    
    """
    return _get_service(host, port, CasperServiceStub, node_id, certificate_file)


def get_control_service(
    host: str,
    port: int,
    node_id: str = None,
    certificate_file: str = None
    ) -> GRPCService:
    """Returns a control service manager.

    :param host: Service host identifier.
    :param port: Port over which service is reachable.
    :param node_id: Node identifier.
    :param certificate_file: Node certificate file used to establish secure handshake.
    
    """
    return _get_service(host, port, ControlServiceStub, node_id, certificate_file)


def _get_service(
    host: str,
    port: int,
    stub: typing.Any,
    node_id: str = None,
    certificate_file: str = None
    ) -> GRPCService:
    """Main factory method.
    
    """
    if node_id:
        with open(certificate_file, "rb") as f:
            credentials = grpc.ssl_channel_credentials(f.read())
        return GRPCService(host, port, stub, credentials, (
            ("grpc.ssl_target_name_override", node_id),
            ("grpc.default_authority", node_id),
        ))
    else:
        return GRPCService(host, port, stub)
