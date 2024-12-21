from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    async def retrieve_data(self): ...
