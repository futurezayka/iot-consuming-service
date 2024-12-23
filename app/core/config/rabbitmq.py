from pydantic import Field

from app.core.config.base import BaseConfig


class RabbitMQConfig(BaseConfig):
    HOST: str = Field("localhost", alias="RABBITMQ_HOST")
    PORT: int = Field(15672, alias="RABBITMQ_PORT")
    USERNAME: str = Field("rmuser", alias="RABBITMQ_USERNAME")
    PASSWORD: str = Field("rmpassword", alias="RABBITMQ_PASSWORD")

    def get_connection_string(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:5672"
