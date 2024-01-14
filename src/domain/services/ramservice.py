"""
This module defines a controller class for fetching RAM values from a monitoring task.
"""
from typing import List
from domain.models import ram
from monitor import MonitorTask


# Controller class to fetch cpu values from monitoring task
class RamService:
    """
    Controller class to fetch RAM values from a monitoring task.
    """

    def __init__(self):
        ...

    async def get_ram(self, monitor_task: MonitorTask) -> List[ram]:
        """
        Get RAM values from the provided monitoring task and return them as a list of Cpu objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch RAM data from.

        Returns:
            List[ram]: A list of Ram objects containing RAM values.
        """
        total = monitor_task.ram_total
        # frequency = ram_available
        frequency = monitor_task.ram_frequency
        ramlist = []
        for i in range(len(monitor_task.ram_percent)):
            available = monitor_task.ram_available[i]
            used = monitor_task.ram_used[i]
            percent = monitor_task.ram_percent[i]
            ramlist.append(ram(total=total, available=available, used=used, percent=percent, frequency=frequency))
        return ramlist

    def __str__(self):
        return self.__class__.__name__
