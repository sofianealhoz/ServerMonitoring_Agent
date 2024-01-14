"""
This module defines a data model for viewed pages information.
"""
from pydantic import BaseModel

class GetViewedPagesResponseSchema(BaseModel): 
    """
    Pydantic data model for representing viewed pages information.

    Attributes:
        url (str): The URL of the viewed page.
        views (int): The number of times the page has been viewed.
    """
    url: str
    views: int