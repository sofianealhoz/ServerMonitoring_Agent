"""
Password hashing and JWT handling.

- Passwords are hashed with bcrypt: slow on purpose and salted, so a stolen table of hashes
  cannot be reversed quickly. The clear password is never stored.
- Access tokens are JWT signed with HS256 and the secret from AGENT_JWT_SECRET. The payload
  is readable by anyone (base64), so it only carries the username, never a password.
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core.config import get_config
from core.exceptions import UnauthorizedException


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def create_access_token(username: str) -> str:
    """Build a signed JWT for this user, valid for access_token_expire_minutes."""
    cfg = get_config()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,  # subject: who the token belongs to
        "iat": now,  # issued at
        "exp": now + timedelta(minutes=cfg.access_token_expire_minutes),  # expiry, checked by jwt.decode
    }
    return jwt.encode(payload, cfg.jwt_secret, algorithm=cfg.jwt_algorithm)


def decode_access_token(token: str) -> str:
    """
    Check the signature and the expiry of a JWT and return its username.

    Raises:
        UnauthorizedException: forged, malformed or expired token.
    """
    cfg = get_config()
    try:
        # algorithms is a whitelist: a token claiming another algorithm (or "none") is refused
        payload = jwt.decode(token, cfg.jwt_secret, algorithms=[cfg.jwt_algorithm])
    except jwt.ExpiredSignatureError as exc:
        raise UnauthorizedException("Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedException("Invalid token") from exc
    username = payload.get("sub")
    if not username:
        raise UnauthorizedException("Invalid token")
    return username
