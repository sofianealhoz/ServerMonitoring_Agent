"""
This module defines a data model for Processus that use a lot
"""
from pydantic import BaseModel


# Processus data model
class Process(BaseModel):
    """
    Pydantic data model for representing Top Processus information.

    Attributes:
        name: The name of the processus.    
        cpu_percent: The CPU usage in percent.
        rss: The RAM usage in MB.
        pid: The PID of the processus.
    """

    name: str
    cpu_percent: float
    rss: float
    pid: int
