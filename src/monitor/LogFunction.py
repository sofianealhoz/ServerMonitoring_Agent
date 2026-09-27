"""
Classe des fonctions utiles pour la récupérations des données des fichiers logs
"""
import logging

from apache_log_parser import LineDoesntMatchException, make_parser  # pip install apache-log-parser
"""
log_co = '/var/log/apache2/other_vhosts_access.log' // sur nos serveurs
local_dir = "Documents"  // Pour les tests
"""

logger = logging.getLogger(__name__)

_parser = make_parser('%h %l %u %t "%r" %>s %b')


def _parsed_lines(log_file_path, newest_first=False):
    """
    Yield (raw line, parsed line) for each valid line of the log file.

    An unreadable file is logged and treated as empty; a malformed line is skipped.
    """
    try:
        with open(log_file_path, "r") as f:
            lines = f.readlines()
    except OSError as exc:
        logger.warning("Cannot read log file %s: %s", log_file_path, exc)
        return
    if newest_first:
        lines.reverse()
    for line in lines:
        try:
            yield line, _parser(line)
        except LineDoesntMatchException:
            logger.debug("Skipping malformed log line: %r", line)


def count_unique_users(log_file_path):
    return len({parsed['remote_logname'] for _line, parsed in _parsed_lines(log_file_path)})


def error404(log_file_path):
    return sum(1 for _line, parsed in _parsed_lines(log_file_path) if parsed['status'] == '404')


def get_last_5_error_logs(log_file_path):
    error_logs = []
    for line, parsed in _parsed_lines(log_file_path, newest_first=True):
        if parsed['status'] == '404':
            error_logs.append(line)
        if len(error_logs) == 5:
            break  # Stop after collecting the last 5 error logs
    return error_logs
