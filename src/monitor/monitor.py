"""This module defines a `MonitorTask` class for monitoring metrics on a host."""
import time
import psutil
import socket
from .LogFunction import count_unique_users, error404, get_last_5_error_logs
from domain.schemas.metrics import MetricSampleSchema
from domain.schemas.network import GetNetworkResponseSchema
from domain.schemas.process import GetTopProcessSchema
from domain.schemas.log import GetLogResponseSchema
from domain.schemas.user import GetUserResponseSchema
from domain.schemas.ram import GetRamResponseSchema
from domain.schemas.hdd import GetHddUsageResponseSchema
from domain.schemas.cpu import GetCpuResponseSchema
from decimal import Decimal

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
    cpu_frequency: float 
    # ram_frequency = ram_available
    ram_frequency: float
    
    # Pour les Log
    unique_users: int 
    nb_error404: int 
    log_directory: str
    last_5_error_logs: list[str]  
    
    # Pour le réseau
    network_statut: psutil.net_io_counters()

    # Pour les processus
    listOfProcessNames = []
    listOfFiveProcessNames = []

    # Pour les infos utilisateur
    nickname: list[str]
    hostname: list[str]
    ip: list[str]

    def __init__(self, publish_metric=None, publish_process=None, publish_network=None, publish_log=None, publish_user=None):
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
        self.nickname = []
        self.hostname = []
        self.ip = []
        # self.cpu_frequency = psutil.cpu_freq().current 
        # ram_available = ram frequency
        self.ram_frequency = psutil.virtual_memory().available
        self.publish_metric = publish_metric or (lambda *_: None)
        self.publish_process = publish_process or (lambda *_: None)
        self.publish_network = publish_network or (lambda *_: None)
        self.publish_log = publish_log or (lambda *_: None)
        self.publish_user = publish_user or (lambda *_: None)


        # On récupère les informations sur l'utilisateur (nickname, hostname, ip)
        for user_info in psutil.users():
            name = user_info.name
            host = user_info.host
            ip = socket.gethostbyname(socket.gethostname())

            self.nickname = self.nickname + [name]
            self.hostname = self.hostname + [host]  
            self.ip = self.ip + [ip]

        self.log_directory = '/var/log/apache2/other_vhosts_access.log' 
        # self.log_directory = "src/monitor/Documents"  # Pour l'instant
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
            self.cpu_frequency = psutil.cpu_freq().current 

            # On récupère les informations sur le disque dur (total, used, free, percent) :
            self.harddrive_usage = psutil.disk_usage('/') 
            self.ram_percent = self.ram_percent + [psutil.virtual_memory().percent]
            self.ram_used = self.ram_used + [psutil.virtual_memory().used / 2**30]
            self.ram_available = self.ram_available + [psutil.virtual_memory().available / 2**30]

            # On récupère les informations des logs (nb ip connectés, nb d'erreurs 404 ) : 
            self.unique_users = self.unique_users + [count_unique_users(self.log_directory)]
            self.nb_error404 = self.nb_error404 + [error404(self.log_directory)]
            self.network_statut = psutil.net_io_counters(pernic=True)
            self.last_5_error_logs = get_last_5_error_logs(self.log_directory)
            
            

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
            
                        # 1) Snapshot global (table metric_samples)
            cpu_usage = sum(self.cpu_percent) / len(self.cpu_percent) if self.cpu_percent else 0.0
            ram_usage = self.ram_percent[-1] if self.ram_percent else 0.0
            disk_usage = self.harddrive_usage.percent if self.harddrive_usage else 0.0

            metric_sample = MetricSampleSchema(
                  # placeholder, la DB générera la vraie clé
                cpu_usage=Decimal(str(cpu_usage)),
                ram_usage=Decimal(str(ram_usage)),
                disk_usage=Decimal(str(disk_usage)),
            )
            self.publish_metric(metric_sample)

            # 2) Réseau : une entrée par interface
            if self.publish_network and self.network_statut:
                for name, stats in self.network_statut.items():
                    network_sample = GetNetworkResponseSchema(
                        name=name,
                        bytes_sent=stats.bytes_sent / 2**20,   # ou en octets si tu préfères
                        bytes_recv=stats.bytes_recv / 2**20,
                        packets_sent=stats.packets_sent,
                        packets_recv=stats.packets_recv,
                        errin=stats.errin,
                        errout=stats.errout,
                        dropin=stats.dropin,
                        dropout=stats.dropout,
                    )
                    self.publish_network(network_sample)

            # 3) Processus (top 5 déjà stockés dans listOfFiveProcessNames)
            if self.publish_process and self.listOfFiveProcessNames:
                for proc in self.listOfFiveProcessNames:
                    process_sample = GetTopProcessSchema(
                        pid=int(proc["pid"]),
                        name=proc["name"],
                        rss=float(proc["rss"]),
                        cpu_percent=float(proc["cpu_percent"]),
                    )
                    self.publish_process(process_sample)

            # 4) Logs Apache
            if self.publish_log:
                log_sample = GetLogResponseSchema(
                    unique_users=int(self.unique_users[-1]) if self.unique_users else 0,
                    nb_error404=int(self.nb_error404[-1]) if self.nb_error404 else 0,
                    last_5_error_logs=self.last_5_error_logs or [],
                )
                self.publish_log(log_sample)

            if self.publish_user and self.nickname:
                for nick, host, ip in zip(self.nickname, self.hostname, self.ip):
                    user_sample = GetUserResponseSchema(
                        nickname=nick,
                        hostname=host,
                        ip=ip,
                    )
                    self.publish_user(user_sample)

            time.sleep(self.interval)
            
    def __str__(self) -> str:
        return f"MonitorTask(interval = {self.interval})"
