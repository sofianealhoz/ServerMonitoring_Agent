import paramiko # pip install paramiko
import apache_log_parser # pip install apache-log-parser
import subprocess
from  pprint import pprint
import re 


username = 'grudu'
hostname1 = "karadoc.telecomste.net"
port1 = 22103
password1 = '103-TgBT-8451'
hostname2 = "mevanwi.telecomste.net"
port2 = 22104
password2 = '104-TgBT-0070'
log_dir = '/var/log/apache2'
log_co = '/var/log/apache2/other_vhosts_access.log'
local_dir = "Documents"

def count_unique_users(log_file_path):
    unique_users = set()

    try:
        # Utilisation de tail pour surveiller les changements en temps réel
        tail_process = subprocess.Popen(['tail', '-f', log_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in iter(tail_process.stdout.readline, b''):
            # Utiliser une expression régulière pour extraire l'adresse IP de la ligne du journal
            match = re.search(r'\d+\.\d+\.\d+\.\d+', line.decode('utf-8'))

            if match:
                ip_address = match.group()
                unique_users.add(ip_address)
                print(ip_address)

            # Affiche le nombre d'utilisateurs uniques à chaque nouvelle ligne dans le journal
            print(f"Nombre d'utilisateurs uniques : {len(unique_users)}", end='\r')

    except KeyboardInterrupt:
        # Arrêt propre si l'utilisateur interrompt le script (Ctrl+C)
        pass
    finally:
        tail_process.terminate()

def parser(log_file_path):
    try:
        f = open(log_file_path,"r")
        lines = f.readlines()
        
        for line in lines :

            line_parser = apache_log_parser.make_parser("%h <<%P>> %t %Dus \"%r\" %>s %b  \"%{Referer}i\" \"%{User-Agent}i\" %l %u")
            pprint(line_parser)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


try:

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
  # Connexion avec mot de passe
    client.connect(hostname1, port1, username, password1)

    with client.open_sftp() as sftp:
        sftp.get(log_co,local_dir)

    #count_unique_users(local_dir)

    parser(local_dir)
        


except Exception as e:
    print(f"Une erreur s'est produite : {e}")

finally:
    # Fermer la connexion SSH
    client.close()