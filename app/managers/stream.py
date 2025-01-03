import asyncio
import json

from aio_pika import Message

from commands.imvoker import DeviceInvoker
from commands.retrieve_data import RetrieveDataCommand
from enums.commands import Commands
from enums.device_type import DeviceType
from enums.queues import Queues
from factory.light import LightSensorFactory
from factory.motion import MotionSensorFactory
from factory.temperature import TemperatureSensorFactory
from schemas.commands import StreamCommand


class StreamManager:
    def __init__(self):
        self.active_streams = dict()
        self.__device_invoker = DeviceInvoker()

    async def process(self, channel, message):
        message = StreamCommand(**json.loads(message.body))
        print(f"Processing message: {message}")
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

        match message.device_type.lower():
            case DeviceType.temperature.value:
                device = TemperatureSensorFactory.create_sensor()
            case DeviceType.light.value:
                device = LightSensorFactory.create_sensor()
            case DeviceType.motion.value:
                device = MotionSensorFactory.create_sensor()
            case _:
                print("Invalid device type")
                return
        self.__device_invoker.add_command(RetrieveDataCommand(device))
        print(f"Starting stream for device: {message.device_id}")
        self.active_streams[message.device_id] = asyncio.create_task(
            self.__start_stream(channel, message.device_id)
        )

    async def __start_stream(self, channel, device_id: str):
        queue = Queues.data.value.format(device_id=device_id)
        await channel.declare_queue(queue, durable=True, auto_delete=False)
        while True:
            data = await self.__device_invoker.execute_commands()
            message = Message(body=data.encode())
            await channel.default_exchange.publish(message, routing_key=queue)
            await asyncio.sleep(5)

    async def __stop_stream(self, channel, device_id: str):
        queue = Queues.data.value.format(device_id=device_id)
        queue = await channel.declare_queue(queue, durable=True, auto_delete=False)
        if device_id in self.active_streams:
            self.active_streams.get(device_id).cancel()
            del self.active_streams[device_id]
            await queue.delete(if_unused=False, if_empty=False)
            print(f"Stream stopped for device: {device_id}")
