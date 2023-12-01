import paramiko 


username = 'grudu'
hostname1 = "karadoc.telecomste.net"
port1 = 22103
passwor1 = '103-TgBT-8451'
hostname2 = "mevanwi.telecomste.net"
port2 = 22104
passwor2 = '104-TgBT-0070'

class MonitorServer: 
    def __init__(self) -> None:
        """
        Initialize the MonitorServer class.

        Add initialization tasks here like checks
        The monitoring interval is 3 seconds.
        """
        self.interval = 3

    def acessServer(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connexion avec mot de passe
            client.connect(hostname1, port1, username, password1)

            # Exécuter une commande (exemple : afficher le répertoire de travail)
            stdin, stdout, stderr = client.exec_command('pwd')
            print("Résultat de la commande :")
            print(stdout.read().decode())

        finally:
            # Fermer la connexion SSH
            client.close()
        