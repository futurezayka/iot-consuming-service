import asyncio

from app.enums.queues import Queues
from app.interfaces.consumer import ABCCommandConsumer
from app.managers.stream import StreamManager


class CommandConsumer(ABCCommandConsumer):
    def __init__(self):
        self.__stream_manager = StreamManager()

    async def consume(self, channel_pool) -> None:
        async with channel_pool.acquire() as channel:
            while True:
                await channel.set_qos(10)

                queue = await channel.declare_queue(
                    Queues.command.value, durable=True, auto_delete=False
                )
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        await message.ack()
                        asyncio.ensure_future(self.process_message(channel, message))
                await asyncio.sleep(0.1)

    async def process_message(self, channel, message):
        try:
            await self.__stream_manager.process(channel, message)
        except Exception as e:
            print(f"Error processing message: {e}")
            await message.nack(requeue=True)
