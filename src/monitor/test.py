import paramiko # pip install paramiko
from apache_log_parser import make_parser # pip install apache-log-parser
import subprocess
from  pprint import pprint
import re 


"""username = 'grudu'
hostname1 = "karadoc.telecomste.net"
port1 = 22103
password1 = '103-TgBT-8451'
hostname2 = "mevanwi.telecomste.net"
port2 = 22104
password2 = '104-TgBT-0070'
log_dir = '/var/log/apache2'
log_co = '/var/log/apache2/other_vhosts_access.log'"""
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

def error404(log_file_path):
    try:
        count404 = 0
        f = open(log_file_path,"r")
        lines = f.readlines()
        
        for line in lines :
            
            parser =make_parser('%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"')
            parser1 = make_parser('%h %l %u %t "%r" %>s %b')
            line_parser = parser1(line)
            
            if (line_parser['status']=='404'):
                count404 +=1
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally :             
        return count404


try:    
    #count_unique_users(local_dir)
    print(error404(local_dir))
        


except Exception as e:
    print(f"Une erreur s'est produite : {e}")

