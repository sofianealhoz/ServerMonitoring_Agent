"""
This module defines a data model for CPU information.
"""
from pydantic import BaseModel


# HDU data model
class Hdd(BaseModel):
    """
    Pydantic data model for representing CPU information.

    Attributes:
        id (int): The ID of the CPU data.
        usage (str): The CPU usage in string format.
    """

    device: str
    mountpoint: str
    fstype: str
    opts: str
    maxfile: int
    maxpath: int

class HddStorage(BaseModel):
    """Pydantic data model for representing HDD usag
    Attributes:
    total (int): The total size of the HDD.
    used (int): The used size of the HDD.
    free (int): The free size of the HDD.
    percent (float): The percentage of the HDD used.
    """
    total: int
    used: int
    free: int
    percent: float