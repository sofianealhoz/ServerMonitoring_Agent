from typing import List
from domain.models import log
from monitor import MonitorTask

log_co = '/var/log/apache2/other_vhosts_access.log'
local_dir = "Documents"


# Controller class to fetch cpu values from monitoring task
class LogService:
    """
    Controller class to fetch RAM values from a monitoring task.
    """

    def __init__(self):
        ...

    async def get_log(self, monitor_task: MonitorTask) -> List[log]:
        """
        Get RAM values from the provided monitoring task and return them as a list of Cpu objects.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch RAM data from.

        Returns:
            List[ram]: A list of Ram objects containing RAM values.
        """
        
        logList = []
        for i in range(len(monitor_task.unique_users)):
            unique_users = monitor_task.unique_users[i]
            nb_error404 = monitor_task.nb_error404[i]
            logList.append(log(unique_users=unique_users, nb_error404=nb_error404))
        return logList
        
    def __str__(self):
        return self.__class__.__name__