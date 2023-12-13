# monitor/monitor.py

import time
import psutil
from .LogFunction import count_unique_users, error404
from domain.services import SystemService  # Importez SystemService ici

class MonitorTask:

    def __init__(self):
        self.interval = 3
        self.num_cores = psutil.cpu_count(logical=False)
        self.ram_percent = []
        self.ram_used = []
        self.ram_available = []
        self.ram_total = psutil.virtual_memory().total / 2**30
        self.unique_users = []
        self.nb_error404 = []
        self.log_directory = "src/monitor/Documents"
        self.network_statut = psutil.net_io_counters()
        self.system_service = SystemService()  # Initialisez SystemService ici

    def update_system_info(self):
        """Update system information in the MonitorTask."""
        system_info = self.system_service.get_system_info()
        # Utilisez les informations du système au besoin

    def monitor(self):
        while True:
            self.cpu_percent = psutil.cpu_percent(percpu=True)
            self.harddrive_usage = psutil.disk_usage('/')
            self.ram_percent.append(psutil.virtual_memory().percent)
            self.ram_used.append(psutil.virtual_memory().used / 2**30)
            self.ram_available.append(psutil.virtual_memory().available / 2**30)
            self.unique_users.append(count_unique_users(self.log_directory))
            self.nb_error404.append(error404(self.log_directory))
            self.network_statut = psutil.net_io_counters(pernic=True)

            self.update_system_info()

            for proc in psutil.process_iter():
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name'])
                    pinfo['cpu_percent'] = proc.cpu_percent(interval=None) / psutil.cpu_count()
                    pinfo['rss'] = proc.memory_info().rss / 2**20
                    self.listOfProcessNames.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            self.listOfProcessNames = sorted(self.listOfProcessNames, key=lambda procObj: procObj['cpu_percent'], reverse=True)
            self.listOfFiveProcessNames = self.listOfProcessNames[:5]

            time.sleep(self.interval)
            
    def __str__(self):
        return f"MonitorTask(interval = {self.interval})"
