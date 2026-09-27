"""
Authentication routes: exchange a username and password for a JWT, and read the current user.
"""
import asyncpg
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from core.exceptions import ForbiddenException, UnauthorizedException
from core.security import create_access_token, verify_password
from dependencies import get_current_user, get_db_connection
from domain.schemas import ExceptionResponseSchema
from domain.schemas.auth import CurrentUserSchema, TokenSchema
from infrastructure.database import fetch_user

auth_router = APIRouter(tags=["auth"])


@auth_router.post(
    "/token",
    response_model=TokenSchema,
    responses={401: {"model": ExceptionResponseSchema}, 403: {"model": ExceptionResponseSchema}},
)
async def login(
    # OAuth2 "password" flow: username and password sent as an HTML form, not as JSON
    form: OAuth2PasswordRequestForm = Depends(),
    conn: asyncpg.Connection = Depends(get_db_connection),
) -> TokenSchema:
    user = await fetch_user(conn, form.username)
    # Same message for an unknown user and a wrong password: do not reveal which accounts exist
    if user is None or not verify_password(form.password, user["hashed_password"]):
        raise UnauthorizedException("Incorrect username or password")
    if user["disabled"]:
        raise ForbiddenException("Account disabled")
    return TokenSchema(access_token=create_access_token(user["username"]))


@auth_router.get(
    "/auth/me",
    response_model=CurrentUserSchema,
    responses={401: {"model": ExceptionResponseSchema}},
)
async def read_me(user: CurrentUserSchema = Depends(get_current_user)) -> CurrentUserSchema:
    """Who am I? Handy to check a token."""
    return user
