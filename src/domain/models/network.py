from pydantic import BaseModel

# Network data model
class Network(BaseModel):
    """
    Pydantic data model for representing network information.

    Attributes:
        bytes_sent (int): The number of bytes sent. 
        bytes_recv (int): The number of bytes received.
        packets_sent (int): The number of packets sent.
        packets_recv (int): The number of packets received.
        errin (int): The number of input errors.
        errout (int): The number of output errors.
        dropin (int): The number of dropped packets on the input.
        dropout (int): The number of dropped packets on the output.
    """
    name: str
    bytes_sent: float
    bytes_recv: float
    packets_sent: int
    packets_recv: int
    errin: int
    errout: int
    dropin: int
    dropout: int