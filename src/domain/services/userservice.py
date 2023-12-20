from typing import List
from domain.models.user import User
from monitor import MonitorTask

class UserService: 
    """
    Controller class to fetch user's info
    """

    def __init__(self):
        ...

    async def get_user(self, monitor_task: MonitorTask) -> List[User]:
        """
        Get user info from the provided monitoring task and return them as a list of users.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch user info.

        Returns:
            List[User]: A list of user objects containing user infos.
        """
        userlist = []
        for i in range(len(monitor_task.nickname)):
            nickname = monitor_task.nickname[i]
            hostname = monitor_task.hostname[i]
            ip = monitor_task.ip[i]
            userlist.append(User(nickname=nickname, hostname=hostname, ip=ip))
        
        print(f"User List: {userlist}")

        return userlist

    def __str__(self):
        return self.__class__.__name__