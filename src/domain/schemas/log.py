"""
This module defines a data model for LOG information.
"""
from pydantic import BaseModel


# LOG data model
class GetLogResponseSchema(BaseModel):
    """
    Pydantic data model for representing LOG information.

    Attributes:
        id (int): The ID of the RAM data.
        usage (str): The RAM usage in string format.
    """

    unique_users: int 
    nb_error404: int