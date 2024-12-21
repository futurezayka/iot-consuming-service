from abc import ABC, abstractmethod


class ABCCommandConsumer(ABC):
    @abstractmethod
    async def consume(self, channel): ...
