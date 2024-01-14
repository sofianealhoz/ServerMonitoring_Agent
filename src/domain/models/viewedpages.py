from pydantic import BaseModel

class ViewedPages(BaseModel):
    """
    Pydantic data model for representing viewed pages information.

    Attributes:
        url (str): The URL of the viewed page.
        views (int): The number of times the page has been viewed.
    """
    url: str
    views: int

    def __str__(self):
        return f"ViewedPages(url={self.url}, views={self.views})"