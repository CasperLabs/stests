import logging
import typing

import grpc

from pyclx.grpc.utils import retry_stream
from pyclx.grpc.utils import retry_unary



class GRPCService():
    """GRPC service manager.
    
    """
    def __init__(
        self,
        host: str,
        port: int,
        stub: typing.Any,
        credentials: grpc.ChannelCredentials = None,
        options: tuple = None):
        """Constructor.

        :param host: Service host identifier.
        :param port: Port over which service is reachable.
        :param stub: Auto-generated GRPC service stub.
        :param credentials: SSL certificate credentials.
        :param options: Channel connection options.
        
        """
        self.address = f"{host}:{port}"
        self.stub = stub
        self.credentials = credentials
        self.options = options


    @property
    def channel_type(self) -> str:
        """Returns type of channel.
        
        """
        return "secure" if self.is_secure else "insecure"

    
    @property
    def is_secure(self) -> bool:
        """Returns flag indicating whether channel is secure at transport layer.
        
        """
        return True if self.credentials else False


    def get_channel(self) -> grpc.Channel:
        """Returns a GRPC channel pointer.
        
        """
        if self.is_secure:
            return grpc.secure_channel(
                self.address,
                self.credentials,
                options=self.options
                )      
        else:  
            return grpc.insecure_channel(self.address)


    def __getattr__(self, name: str) -> typing.Callable:
        """Attribute accessor invoked when executing a GRPC service endpoint.
        
        """
        logging.debug(
            f"GRPC :: {self.channel_type} channel :: open -> {self.address} ({self.stub})"
        )

        @retry_unary
        def unary_unary(*args) -> typing.Any:
            """Endpoint executor: unary to unary."""
            logging.debug(
                f"GRPC :: {self.channel_type} channel :: execute -> {self.address} ({self.stub}): {name} {list(args)}"
            )
            with self.get_channel() as channel:
                return getattr(self.stub(channel), name)(*args)

        @retry_stream
        def unary_stream(*args) -> typing.Any:
            """Endpoint executor: unary to stream."""
            logging.debug(
                f"GRPC :: {self.channel_type} channel :: execute -> {self.address} ({self.stub}): {name} {list(args)}"
            )            
            name = name[: -len("_stream")]
            with self.get_channel() as channel:
                yield from getattr(self.stub(channel), name)(*args)

        return unary_stream if name.endswith("_stream") else unary_unary
