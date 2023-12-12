from typing import List
from domain.models import Process
from monitor import MonitorTask


class ProcessService:

    def __init__(self):
        ...

    async def get_process(self, monitor_task: MonitorTask) -> List[Process]:
        
        """
        Get  process values from the provided monitoring task and return the 5 biggest as a list of Process objects.
    
        Args:
            monitor_task (MonitorTask): The monitoring task to fetch process data from.

        Returns:
            List[process]: A list of Process objects containing process values.
        """
        # Iterate over the list

        # Sort list of dict by key vms i.e. memory usage
        processlist = []
        for proc in monitor_task.listOfFiveProcessNames:
            processlist.append(Process(pid=proc['pid'], name=proc['name'], rss=proc['rss'], cpu_percent=proc['cpu_percent']))
        return processlist
        
