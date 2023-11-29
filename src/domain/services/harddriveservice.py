from typing import List
from domain.models import Hdd
from monitor import MonitorTask
#import psutil._common.sdiskpart as sdiskpart

class HardDriveService:
    def __init__(self):
        ...

    async def get_harddrive_usage(self, monitor_task: MonitorTask) -> List[Hdd]:
        """Get the current usage of each disk on the system."""
        hdd_list = [Hdd]

        """for i in range(len(monitor_task.harddrive_part)):
            hdd_list.append(Hdd(device=monitor_task.harddrive_part[i].device, mountpoint=monitor_task.harddrive_part[i].mountpoint, fstype=monitor_task.harddrive_part[i].fstype, opts=monitor_task.harddrive_part[i].opts, maxfile=monitor_task.harddrive_part[i].maxfile, maxpath=monitor_task.harddrive_part[i].maxpath))
        return hdd_list"""
        for i in range(5):
            hdd_list.append(Hdd(device="bonjour", mountpoint="emile", fstype="aaa", opts="sss", maxfile=int(255), maxpath=int(321)))
        return hdd_list
        
    def __str__(self):
        return self.__class__.__name__