# services/system_service.py

from domain.models import SystemInfo
import socket
import requests

class SystemService:
    """
    Controller class to fetch system information.
    """

    async def get_system_info(self) -> SystemInfo:
        """
        Get system information and return a SystemInfo object.

        Returns:
            SystemInfo: An object containing system information.
        """
        nickname = "MonNickname"  # Remplacez par votre logique réelle pour obtenir le surnom
        hostname = socket.gethostname()

        local_ip = self.get_local_ip()
        public_ip = await self.get_public_ip()

        return SystemInfo(nickname=nickname, hostname=hostname, local_ip=local_ip, public_ip=public_ip)

    def get_local_ip(self) -> str:
        """
        Get the local IP address of the machine.

        Returns:
            str: The local IP address.
        """
        return socket.gethostbyname(socket.gethostname())

    async def get_public_ip(self) -> str:
        """
        Get the public IP address of the machine.

        Returns:
            str: The public IP address.
        """
        try:
            response = await requests.get('https://httpbin.org/ip')
            return response.json()['origin']
        except Exception as e:
            # Gérer les erreurs, par exemple, si la demande échoue
            print(f"Erreur lors de la récupération de l'adresse IP publique : {e}")
            return "Erreur"

    def __str__(self):
        return self.__class__.__name__
