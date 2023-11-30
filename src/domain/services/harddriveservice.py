from typing import List
from domain.models import Hdd
from monitor import MonitorTask
#import psutil._common.sdiskpart as sdiskpart

class HardDriveService:

    hdd_usage: Hdd

    def __init__(self):
        ...

    async def get_harddrive_usage(self, monitor_task: MonitorTask) -> List[Hdd]:
        """Get the current usage of each disk on the system."""

        """for i in range(len(monitor_task.harddrive_part)):
            hdd_list.append(Hdd(device=monitor_task.harddrive_part[i].device, mountpoint=monitor_task.harddrive_part[i].mountpoint, fstype=monitor_task.harddrive_part[i].fstype, opts=monitor_task.harddrive_part[i].opts, maxfile=monitor_task.harddrive_part[i].maxfile, maxpath=monitor_task.harddrive_part[i].maxpath))
        return hdd_list"""

        #On récupère les valeurs, sous le tyep sdiskpart
        self.hdd_usage = monitor_task.harddrive_usage

        #On convertit les valeurs en Go (les int de "sdiskpart" sont donc convertit en float)
        hdd_use = Hdd(total=self.hdd_usage.total / 2**30, used=self.hdd_usage.used / 2**30, free=self.hdd_usage.free / 2**30, percent=self.hdd_usage.percent)       
        
        return hdd_use
        
    def __str__(self):
        return self.__class__.__name__