from typing import List
from domain.models import Network
from monitor import MonitorTask
import psutil

class NetworkService:

    network_statu: Network
    network_recup: psutil.net_io_counters()
    def __init__(self):
        ...

    async def get_network_statut(self, monitor_task: MonitorTask) -> List[Network]:
        """Get the current usage of each disk on the system."""
        listNetwork = []
        self.network_recup = monitor_task.network_statut
        for key in self.network_recup.keys():
            listNetwork.append(Network(
            name = key,
            bytes_sent=self.network_recup[key].bytes_sent / 2**20, #Conversion en Mo.
            bytes_recv=self.network_recup[key].bytes_recv / 2**20,
            packets_sent=self.network_recup[key].packets_sent,
            packets_recv=self.network_recup[key].packets_recv,
            errin=self.network_recup[key].errin,
            errout=self.network_recup[key].errout,
            dropin=self.network_recup[key].dropin,
            dropout=self.network_recup[key].dropout
            ))
        return listNetwork