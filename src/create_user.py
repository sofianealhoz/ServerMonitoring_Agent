"""
Create an API account.

Usage: python3 src/create_user.py <username> <reader|admin>
The password is typed interactively (never passed on the command line, where it would land in
the shell history) and stored hashed with bcrypt.
"""
import asyncio
import getpass
import sys

import asyncpg

from core.config import get_config
from core.security import hash_password


async def create_user(username: str, role: str, password: str) -> None:
    conn = await asyncpg.connect(get_config().database_url)
    try:
        await conn.execute(
            "INSERT INTO users (username, hashed_password, role) VALUES ($1, $2, $3)",
            username, hash_password(password), role,
        )
    finally:
        await conn.close()


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[2] not in ("reader", "admin"):
        sys.exit("Usage: python3 src/create_user.py <username> <reader|admin>")
    username, role = sys.argv[1], sys.argv[2]
    password = getpass.getpass("Password: ")
    if password != getpass.getpass("Confirm password: "):
        sys.exit("Passwords do not match")
    asyncio.run(create_user(username, role, password))
    print(f"User {username} created with role {role}")


if __name__ == "__main__":
    main()
