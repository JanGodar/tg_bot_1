from pydantic import SecretStr, RedisDsn
from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    bot_token: SecretStr
    redis_dsn: RedisDsn