"""
This module defines a data model for Processus that use a lot
"""
from pydantic import BaseModel


# RAM data model
class topProcess(BaseModel):
    """
    Pydantic data model for representing RAM information.

    Attributes:
        id (int): The ID of the RAM data.
        usage (str): The RAM usage in string format.
    """

    total: float  # en Go
    available: float
    used: float
    percent: float
