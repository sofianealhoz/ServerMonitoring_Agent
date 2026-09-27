"""
This module defines a controller class for fetching CPU values from a monitoring task.
"""
from typing import List
from core.exceptions import ServiceUnavailableException
from domain.models import Cpu
from monitor import MonitorTask


# Controller class to fetch cpu values from monitoring task
class CpuService:
    """
    Controller class to fetch CPU values from a monitoring task.
    """

    def __init__(self):
        ...

    async def get_cpu(self, monitor_task: MonitorTask) -> List[Cpu]:
        """
        Get CPU values from the provided monitoring task and return them as a list of Cpu objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch CPU data from.

        Returns:
            List[Cpu]: A list of Cpu objects containing CPU values.

        Raises:
            ServiceUnavailableException: The monitoring thread has not collected CPU data yet.
        """
        if getattr(monitor_task, "cpu_percent", None) is None:
            raise ServiceUnavailableException("CPU metrics not collected yet, retry in a few seconds")
        cpulist = []
        for core, usage in enumerate(monitor_task.cpu_percent):
            cpulist.append(Cpu(id=core, usage=str(usage), frequency=monitor_task.cpu_frequency))
        return cpulist

    def __str__(self):
        return self.__class__.__name__
