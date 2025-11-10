"""
This module contains configuration classes and functions for the Agent application.

It defines the `Config` class, which contains configuration parameters, and subclasses
`LocalConfig` and `ProductionConfig` for specific environment configurations. It also provides
a `get_config` function to retrieve the appropriate configuration based on the environment.
"""
import os
import contextvars
from dataclasses import dataclass

config = contextvars.ContextVar("configuration", default=None)

database_async_url: str = "postgresql+asyncpg://postgreuser:postgrepswd@localhost:5432/dbname_monitoring"

@dataclass
class Config:
    """Default configuration class for the Agent application."""

    version: str
    description: str
    database_url: str
    title: str = "Agent"
    env: str = "production"
    debug: bool = False
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    database_pool_size: int = 5
    database_max_overflow: int = 10

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


def get_config() -> Config:
    """
    Get the appropriate configuration based on the environment.

    Returns:
        Config: The configuration object for the current environment.
    """
    env = os.getenv("AGENT_ENV", "production")
    version = os.getenv("AGENT_VERSION", "1.0.0")
    description = os.getenv("AGENT_DESCRIPTION", "api for python agent")
    debug = bool(os.getenv("AGENT_DEBUG", "False"))
    database_url = database_async_url
    match env:
        case "local":
            cfg = LocalConfig(version=version, description=description)
        case _:
            cfg = ProductionConfig(
                version=version, description=description, debug=debug, database_url=database_url
            )
    return cfg
