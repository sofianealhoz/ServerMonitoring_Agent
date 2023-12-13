from pydantic import BaseModel

class GetSystemInfoResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing system information.

    Attributes:
        nickname (str): The nickname of the system.
        hostname (str): The hostname of the system.
        ip_address (str): The IP address of the system.
    """

    nickname: str
    hostname: str
    ip_address: str