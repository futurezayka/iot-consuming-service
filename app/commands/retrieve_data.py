from interfaces.command import Command
from interfaces.device import Device


class RetrieveDataCommand(Command):
    def __init__(self, device: Device):
        self.device = device

    async def execute(self):
        return await self.device.retrieve_data()
