from pydantic import BaseModel


class GetTopProcessSchema(BaseModel):
    """
    Pydantic data model for the response schema representing Top Processus information.

    Attributes:
        name: The name of the processus.    
        cpu_percent: The CPU usage in percent.
        rss: The RAM usage in MB.
        pid: The PID of the processus.
    """

    pid: int
    name: str
    rss: float
    cpu_percent: float
    
    