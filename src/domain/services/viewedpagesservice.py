from typing import List
from domain.models.viewedpages import ViewedPages
from monitor import MonitorTask

class ViewedPagesService: 
    """
    Controller class to fetch viewed pages' info
    """

    def __init__(self):
        ...

    async def get_most_viewed_page(self, monitor_task: MonitorTask) -> ViewedPages:
        """
        Get most viewed pages' info from the provided monitoring task and return them as a ViewedPages.

        Args:
            monitor_task (MonitorTask): The monitoring task to fetch viewed pages' info.

        Returns:
            ViewedPages: A ViewedPages object containing viewed pages' info.
        """
        url = monitor_task.url
        views = monitor_task.views
        viewedpages = ViewedPages(url=url, views=views)

        return viewedpages

    def __str__(self):
        return self.__class__.__name__