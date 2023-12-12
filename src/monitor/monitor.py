"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil
from .LogFunction import count_unique_users, error404


class MonitorTask:

    """A class for monitoring metrics."""
    interval: int
    cpu_percent: list[float]
    ram_percent: list[int]
    num_cores: int
    harddrive_usage: psutil.disk_usage('/')
    ram_used: list[float] 
    ram_available: list[float] 
    ram_total: float
    
    # Pour les Log
    unique_users: int 
    nb_error404: int 
    log_directory: str
    
    # Pour le réseau
    network_statut: psutil.net_io_counters()

    # Pour les processus
    listOfProcessNames = []
    listOfFiveProcessNames = []

    def __init__(self) -> None:
        """
        Initialize the MonitorTask class.

        Add initialization tasks here like checks
        The monitoring interval is 3 seconds.
        """
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        self.ram_percent = []
        self.ram_used = []
        self.ram_available = []
        self.ram_total = psutil.virtual_memory().total / 2**30
        self.unique_users = []
        self.nb_error404 = []

        # self.log_directory = '/var/log/apache2/other_vhosts_access.log' Pour les serveurs
        self.log_directory = "src/monitor/Documents"  # Pour l'instant
        self.network_statut = psutil.net_io_counters(pernic=True)

        for proc in psutil.process_iter():
            try:
                proc.cpu_percent(interval=None)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def monitor(self):
        """Continuously monitor and store the result in an attribute."""
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)   

            # On récupère les informations sur le disque dur (total, used, free, percent) :
            self.harddrive_usage = psutil.disk_usage('/') 
            self.ram_percent = self.ram_percent + [psutil.virtual_memory().percent]
            self.ram_used = self.ram_used + [psutil.virtual_memory().used / 2**30]
            self.ram_available = self.ram_available + [psutil.virtual_memory().available / 2**30]

            # On récupère les informations des logs (nb ip connectés, nb d'erreurs 404 ) : 
            self.unique_users = self.unique_users + [count_unique_users(self.log_directory)]
            self.nb_error404 = self.nb_error404 + [error404(self.log_directory)]
            self.network_statut: psutil.net_io_counters(pernic=True)

            # On récupère les informations sur les processus (pid, name, rss, cpu_percent) :
            for proc in psutil.process_iter():
                try:
                    # Fetch process details as dict
                    pinfo = proc.as_dict(attrs=['pid', 'name'])
                    pinfo['cpu_percent'] = proc.cpu_percent(interval=None) / psutil.cpu_count()
                    pinfo['rss'] = proc.memory_info().rss / 2**20
                    # Append dict to list
                    self.listOfProcessNames.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            # Edit procObj[...] : 'rss' pour la mémoire, 'cpu_percent' pour le CPU
            self.listOfProcessNames = sorted(self.listOfProcessNames, key=lambda procObj: procObj['cpu_percent'], reverse=True)
            self.listOfFiveProcessNames = self.listOfProcessNames[:5]

            time.sleep(self.interval)
            
    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"
