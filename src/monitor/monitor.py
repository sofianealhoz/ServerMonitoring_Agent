"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil._common
import psutil 



class MonitorTask:
    """A class for monitoring metrics."""

    
    interval: int
    cpu_percent: list[float]
    num_cores: int
    harddrive_part: list[psutil._common.sdiskpart]
    
    def __init__(self) -> None:
        """
        Initialize the MonitorTask class.

        Add initialization tasks here like checks
        The monitoring interval is 3 seconds.
        """
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        

    def monitor(self):
        """Continuously monitor and store the result in an attribute."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.harddrive_part = (psutil.disk_partitions(all=False))
            #self.harddrive_usage.append(psutil.disk_usage('/'))
            time.sleep(self.interval)

    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"
