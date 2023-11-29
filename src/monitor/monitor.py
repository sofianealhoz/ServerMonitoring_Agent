"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil


class MonitorTask:
    """A class for monitoring metrics."""

    
    interval: int
    cpu_percent: list[float]
    ram_percent: list[int]
    num_cores: int
    ram_used : list[float] 
    ram_available : list[float] 
    ram_total : float

    def __init__(self) -> None:
        """
        Initialize the MonitorTask class.

        Add initialization tasks here like checks
        The monitoring interval is 3 seconds.
        """
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        self.ram_percent =[]
        self.ram_used= []
        self.ram_available =[]
        self.ram_total = psutil.virtual_memory().total/1000000000

    def monitor(self):
        """Continuously monitor and store the result in an attribute."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.ram_percent= self.ram_percent + [psutil.virtual_memory().percent]
            self.ram_used = self.ram_used + [psutil.virtual_memory().used/1000000000]
            self.ram_available = self.ram_available + [psutil.virtual_memory().available/1000000000]
            time.sleep(self.interval)

    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"
