from pydantic import BaseModel


class GetHddUsageResponseSchema(BaseModel):
    """Pydantic data model for the response schema representing HDD information.

    Attributes:
        total (float): The total size of the HDD.
        used (float): The used size of the HDD.
        free (float): The free size of the HDD.
        percent (float): The percentage of the HDD used.
    """
    # Tout est en float pour pouvoir obtenir les valeurs en Go.
    total: float
    used: float
    free: float
    percent: float
