from pydantic import BaseModel

class GetHddResponseSchema(BaseModel):
    """
    Pydantic data model for the response schema representing HDD information.

    Attributes:
        id (int): The ID of the HDD data.
        usage (str): The HDD usage in string format.
    """

    device: str
    mountpath: str
    fstype: str
    opts: str
    maxfile: int
    maxpath: int

"""class GetHddPartResponseSchema(BaseModel):
    
    Pydantic data model for the response schema representing HDD information.

    Attributes:
        id (int): The ID of the HDD data.
        usage (str): The HDD usage in string format.
    
    name: str"""
    