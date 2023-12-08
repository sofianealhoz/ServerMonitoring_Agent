"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil
from LogFunction import count_unique_users, error404



class MonitorTask:
    """A class for monitoring metrics."""

    
    interval: int
    cpu_percent: list[float]
    ram_percent: list[int]
    num_cores: int
    harddrive_usage: psutil.disk_usage('/')
    ram_used : list[float] 
    ram_available : list[float] 
    ram_total : float
    

    # Pour les Log
    unique_users : int 
    nb_error404 : int 
    log_directory : str
    logger : LogFunction

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
        self.ram_total = psutil.virtual_memory().total/2**30
        self.unique_users = []
        self.nb_error404 = []
        #self.log_directory = '/var/log/apache2/other_vhosts_access.log' Pour les serveurs
        self.log_directory = "Documents" # Pour l'instant

    def monitor(self):
        """Continuously monitor and store the result in an attribute."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)            
            #On récupère les informations sur le disque dur (total, used, free, percent) :
            self.harddrive_usage = psutil.disk_usage('/') 
            self.ram_percent= self.ram_percent + [psutil.virtual_memory().percent]
            self.ram_used = self.ram_used + [psutil.virtual_memory().used/2**30]
            self.ram_available = self.ram_available + [psutil.virtual_memory().available/2**30]
            # On récupère les informations des logs (nb ip connectés, nb d'erreurs 404 ) : 
            self.unique_users = self.unique_users + [count_unique_users(self.log_directory)]
            self.nb_error404 = self.nb_error404 + [error404(self.log_directory)]
            time.sleep(self.interval)
            

    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"
