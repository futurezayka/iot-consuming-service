from abc import abstractmethod, ABC


class ABCRabbitMQService(ABC):

    @abstractmethod
    async def _create_connection(self) -> None: ...

    @abstractmethod
    async def _consume_messages(self) -> None: ...

    @abstractmethod
    async def close_connection(self) -> None: ...
