import asyncio

from aio_pika import connect_robust, Channel
from aio_pika.pool import Pool

from app.consumers.command import CommandConsumer
from app.core import settings
from app.decorators.retry import retry
from app.interfaces.consumer import ABCCommandConsumer
from app.interfaces.rabbitmq import ABCRabbitMQService


class RabbitMQService(ABCRabbitMQService):
    def __init__(self, command_consumer: ABCCommandConsumer):
        self.__config = settings.rabbitmq
        self.__consumer = command_consumer or CommandConsumer()
        self.__connection_pool = None

    @retry(max_retries=10, delay=2)
    async def _create_connection(self):
        return await connect_robust(self.__config.get_connection_string())

    async def _create_connection_pool(self) -> None:
        loop = asyncio.get_event_loop()
        self.__connection_pool = Pool(self._create_connection, max_size=10, loop=loop)

    async def close_connection(self) -> None:
        for connection in self.__connection_pool:
            await connection.close()

    async def _consume_messages(self) -> None:
        loop = asyncio.get_event_loop()
        channel_pool = Pool(self._get_channel, max_size=10, loop=loop)
        await loop.create_task(self.__consumer.consume(channel_pool=channel_pool))

    async def start(self) -> None:
        await self._create_connection_pool()
        await self._consume_messages()

    async def _get_channel(self) -> Channel:
        async with self.__connection_pool.acquire() as connection:
            return await connection.channel()


def rabbitmq_service() -> RabbitMQService:
    return RabbitMQService(
        command_consumer=CommandConsumer()
    )
