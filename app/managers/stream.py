import asyncio
import json
from uuid import UUID

from aio_pika import Message

from commands.imvoker import DeviceInvoker
from commands.retrieve_data import RetrieveDataCommand
from devices.temperature import TemperatureSensor
from enums.queues import Queues
from schemas.commands import StreamCommand


class StreamManager:
    def __init__(self):
        self.active_streams = dict()

    async def process(self, channel, message):
        message = StreamCommand(**json.loads(message.body))
        print(self.active_streams)
        match message.type:
            case "start_stream":
                await self.process_device(channel, message)
            case "stop_stream":
                await self.__stop_stream(channel, message.device_id)

    async def process_device(self, channel, message):
        invoker = DeviceInvoker()
        match message.device_type:
            case "temperature":
                device = TemperatureSensor()
                command = RetrieveDataCommand(device)
                invoker.add_command(command)
            case "light":
                ...
        if message.device_id not in self.active_streams:
            print(f"Starting stream for device: {message.device_id}")
            self.active_streams[message.device_id] = asyncio.create_task(
                self.__start_stream(channel, message.device_id, invoker)
            )

    async def __start_stream(self, channel, device_id: UUID, invoker: DeviceInvoker):
        queue = Queues.data.value.format(device_id=device_id)
        await channel.declare_queue(queue, durable=True, auto_delete=False)
        while True:
            data = await invoker.execute_commands()
            message = Message(body=str(data).encode())
            await channel.default_exchange.publish(message, routing_key=queue)
            await asyncio.sleep(1)

    async def __stop_stream(self, channel, device_id: UUID):
        queue = Queues.data.value.format(device_id=device_id)
        queue = await channel.declare_queue(queue, durable=True, auto_delete=False)
        if device_id in self.active_streams:
            self.active_streams.get(device_id).cancel()
            del self.active_streams[device_id]
            await queue.delete(if_unused=False, if_empty=False)
            print(f"Stream stopped for device: {device_id}")
