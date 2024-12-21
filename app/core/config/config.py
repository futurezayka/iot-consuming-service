from app.core.config.base import BaseConfig
from app.core.config.rabbitmq import RabbitMQConfig

__all__ = ["settings"]


class Settings(BaseConfig):
    rabbitmq: RabbitMQConfig = RabbitMQConfig()


settings = Settings()
