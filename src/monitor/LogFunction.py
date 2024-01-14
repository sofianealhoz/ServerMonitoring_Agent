from apache_log_parser import make_parser, LineDoesntMatchException

def count_unique_users(log_file_path):
    unique_users = 0
    ip_set = set()
    try:
        with open(log_file_path, "r") as f:
            parser = make_parser('%h %l %u %t "%r" %>s %b')
            for line in f:
                try:
                    line_parser = parser(line)
                    ip = line_parser['remote_host'] or line_parser['host']
                    if ip:
                        ip_set.add(ip)
                except LineDoesntMatchException:
                    continue

        unique_users = len(ip_set)

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return unique_users

def error404(log_file_path):
    count404 = 0
    try:
        with open(log_file_path, "r") as f:
            parser = make_parser('%h %l %u %t "%r" %>s %b')
            for line in f:
                try:
                    line_parser = parser(line)
                    if line_parser['status'] == '404':
                        count404 += 1
                except LineDoesntMatchException:
                    continue

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    return count404

log_file_path = '/var/log/apache2/access.log'  # Remplacez cela par le chemin réel de votre fichier log
print("Nombre d'utilisateurs uniques:", count_unique_users(log_file_path))
print("Nombre d'erreurs 404:", error404(log_file_path))
