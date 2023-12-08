"""

"""



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
    unique_users = 0

    try:
        ipList = []
        f = open(log_file_path,"r")
        lines = f.readlines()
    
        for line in lines :
            parser1 = make_parser('%h %l %u %t "%r" %>s %b')
            line_parser = parser1(line)
                
            if len(ipList) == 0 :
                ipList.append(line_parser['remote_logname'])
            else :
                if line_parser['remote_logname'] not in ipList :
                    ipList.append(line_parser['remote_logname'])
        unique_users = len(ipList)
        
                
            
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally:
        return unique_users

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

            print(type(line_parser['remote_logname']))
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
    finally :             
        return count404


print(count_unique_users(local_dir))


