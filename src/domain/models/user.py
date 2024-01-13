"""
This module defines a data model for user information.
"""
from pydantic import BaseModel

class User(BaseModel):
    """
    Pydantic data model for representing user information.

    Attributes:
        nickname (str): The nickname of the user.
        hostname (str): The hostname of the user.
        ip (str): The ip adress of the user. 
    """
    nickname: str
    hostname: str
    ip: str


    def __str__(self):
        return f"User(nickname={self.nickname}, hostname={self.hostname}, ip={self.ip})"