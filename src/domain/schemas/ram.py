"""
This module defines a data transfer model for a GetRamResponseSchema.
"""
from pydantic import BaseModel


class GetRamResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing RAM information.

    Attributes:
        id (int): The ID of the RAM data.
        usage (str): The RAM usage in string format.
    """

    id: int
    usage: str


class GetRamCoreResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing RAM core number.

    Attributes:
        number (int): RAM core number.
    """

    number: int