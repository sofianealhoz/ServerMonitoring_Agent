from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Response of POST /token, in the format defined by OAuth2."""

    access_token: str
    token_type: str = "bearer"


class CurrentUserSchema(BaseModel):
    """The authenticated user, injected into routes by get_current_user."""

    username: str
    role: str
