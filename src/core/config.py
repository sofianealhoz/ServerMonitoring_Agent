"""
This module contains configuration classes and functions for the Agent application.

It defines the `Config` class, which contains configuration parameters, and subclasses
`LocalConfig` and `ProductionConfig` for specific environment configurations. It also provides
a `get_config` function to retrieve the appropriate configuration based on the environment.

Secrets (database URL with its password, JWT signing key) are never written in the code: they
come from environment variables. See .env.example.
"""
import os
import contextvars
from dataclasses import dataclass

config = contextvars.ContextVar("configuration", default=None)


@dataclass
class Config:
    """Default configuration class for the Agent application."""

    version: str
    description: str
    database_url: str
    jwt_secret: str
    title: str = "Agent"
    env: str = "production"
    debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_pool_size: int = 5
    database_max_overflow: int = 10
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

@dataclass
class LocalConfig(Config):
    """Local configuration class for the Agent application."""

    title: str = "Agent - local"
    env: str = "local"
    debug: str = True


@dataclass
class ProductionConfig(Config):
    """Production configuration class for the Agent application."""

    debug: str = False


def _require_env(name: str) -> str:
    """Read a mandatory environment variable, or stop with a clear message."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing environment variable {name} (see .env.example)")
    return value


def get_config() -> Config:
    """
    Get the appropriate configuration based on the environment.

    Returns:
        Config: The configuration object for the current environment.
    """
    env = os.getenv("AGENT_ENV", "production")
    version = os.getenv("AGENT_VERSION", "1.0.0")
    description = os.getenv("AGENT_DESCRIPTION", "api for python agent")
    debug = os.getenv("AGENT_DEBUG", "False") == "True"
    secrets = {
        "database_url": _require_env("AGENT_DATABASE_URL"),
        "jwt_secret": _require_env("AGENT_JWT_SECRET"),
    }
    match env:
        case "local":
            cfg = LocalConfig(version=version, description=description, **secrets)
        case _:
            cfg = ProductionConfig(version=version, description=description, debug=debug, **secrets)
    return cfg
