from interfaces.command import Command


class DeviceInvoker:
    def __init__(self):
        self.commands = []

    def add_command(self, command: Command):
        self.commands.append(command)

    async def execute_commands(self):
        for command in self.commands:
            return await command.execute()
