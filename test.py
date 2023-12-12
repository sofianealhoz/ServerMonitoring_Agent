import psutil

def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent'])
           pinfo['rss'] = proc.memory_info().rss / 2**20
           # Append dict to list
           listOfProcObjects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['rss'], reverse=True)

    return listOfProcObjects

listOfProcObjects = getListOfProcessSortedByMemory()
listOfFiveProc = listOfProcObjects[:5]
for proc in listOfFiveProc:
    print(proc)