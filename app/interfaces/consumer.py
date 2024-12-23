from abc import ABC, abstractmethod


class ABCCommandConsumer(ABC):
    @abstractmethod
    async def consume(self, channel): ...

    @abstractmethod
    async def _process_message(self, channel, message): ...
