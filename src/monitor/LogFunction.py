"""
Classe des fonctions utiles pour la récupérations des données des fichiers logs
"""
from apache_log_parser import make_parser  # pip install apache-log-parser
"""
log_co = '/var/log/apache2/other_vhosts_access.log' // sur nos serveurs
local_dir = "Documents"  // Pour les tests
"""


def count_unique_users(log_file_path):
    unique_users = 0

    try:
        ipList = []
        f = open(log_file_path, "r")
        lines = f.readlines()
    
        for line in lines:
            parser1 = make_parser('%h %l %u %t "%r" %>s %b')
            line_parser = parser1(line)
                
            if len(ipList) == 0:
                ipList.append(line_parser['remote_logname'])
            else:
                if line_parser['remote_logname'] not in ipList:
                    ipList.append(line_parser['remote_logname'])
        unique_users = len(ipList)
    except KeyboardInterrupt:
        # Arrêt propre si l'utilisateur interrompt le script (Ctrl+C)
        pass
    finally:
        return unique_users


def error404(log_file_path):
    try:
        count404 = 0
        f = open(log_file_path, "r")
        lines = f.readlines()
        
        for line in lines:
            parser1 = make_parser('%h %l %u %t "%r" %>s %b')
            line_parser = parser1(line)

            if (line_parser['status'] == '404'):
                count404 += 1

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:             
        return count404


        