from abc import abstractmethod, ABC


class Command(ABC):
    @abstractmethod
    async def execute(self): ...
