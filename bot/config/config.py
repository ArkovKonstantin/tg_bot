from os import environ
from pathlib import Path

from pydantic import BaseSettings

PROJECT_PATH = Path(__file__).parent.parent.parent.resolve()


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "local")
    TOKEN: str = environ.get("TOKEN")

    NATS_HOST: str = environ.get("NATS_HOST", "0.0.0.0")
    NATS_PORT: int = int(environ.get("NATS_PORT", "80"))

    @property
    def nats_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "host": self.NATS_HOST,
            "port": self.NATS_PORT,
        }

    @property
    def nats_uri(self) -> str:
        """
        Get uri for connection with nats.
        """
        return "nats://{host}:{port}".format(
            **self.nats_settings,
        )

    class Config:
        env_file = str(PROJECT_PATH.joinpath(".env"))
        env_file_encoding = "utf-8"


print(str(PROJECT_PATH.joinpath(".env")))

def get_settings() -> DefaultSettings:
    env = environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()
    # ...
    # space for other settings
    # ...
    return DefaultSettings()  # fallback to default
