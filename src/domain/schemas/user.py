"""
This module defines a data model for user information.
"""
from pydantic import BaseModel

class GetUserResponseSchema(BaseModel):
    """
    Pydantic data model for representing LOG information.

    Attributes:
        nickname (str): The nickname of the user.
        hostname (str): The hostname of the user.
        ip (str): The ip adress of the user. 
    """

    nickname: str 
    hostname: str
    ip: str
