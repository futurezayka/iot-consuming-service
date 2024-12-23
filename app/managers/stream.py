import asyncio
import json
from uuid import UUID

from aio_pika import Message

from commands.imvoker import DeviceInvoker
from commands.retrieve_data import RetrieveDataCommand
from devices.light import LightSensor
from devices.motion import MotionSensor
from devices.temperature import TemperatureSensor
from enums.commands import Commands
from enums.device_type import DeviceType
from enums.queues import Queues
from schemas.commands import StreamCommand


class StreamManager:
    def __init__(self):
        self.active_streams = dict()
        self.__device_invoker = DeviceInvoker()

    async def process(self, channel, message):
        message = StreamCommand(**json.loads(message.body))
        match message.type:
            case Commands.start_stream.value:
                await self.process_device(channel, message)
            case Commands.stop_stream.value:
                await self.__stop_stream(channel, message.device_id)
            case _:
                print("Invalid command")
                return

    async def process_device(self, channel, message):
        if message.device_id in self.active_streams:
            print(f"Stream already active for device: {message.device_id}")
            return

        match message.device_type:
            case DeviceType.temperature.value:
                device = TemperatureSensor()
            case DeviceType.light.value:
                device = LightSensor()
            case DeviceType.motion.value:
                device = MotionSensor()
            case _:
                print("Invalid device type")
                return
        self.__device_invoker.add_command(RetrieveDataCommand(device))
        print(f"Starting stream for device: {message.device_id}")
        self.active_streams[message.device_id] = asyncio.create_task(
            self.__start_stream(channel, message.device_id)
        )

    async def __start_stream(self, channel, device_id: UUID):
        queue = Queues.data.value.format(device_id=device_id)
        await channel.declare_queue(queue, durable=True, auto_delete=False)
        while True:
            data = await self.__device_invoker.execute_commands()
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
