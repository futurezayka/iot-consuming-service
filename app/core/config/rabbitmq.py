from pydantic import Field

from app.core.config.base import BaseConfig


class RabbitMQConfig(BaseConfig):
    HOST: str = Field("localhost", alias="RABBITMQ_HOST")
    PORT: int = Field(..., alias="RABBITMQ_PORT")
    USERNAME: str = Field(..., alias="RABBITMQ_USERNAME")
    PASSWORD: str = Field(..., alias="RABBITMQ_PASSWORD")

    def get_connection_string(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:5672"
