from abc import abstractmethod, ABC


class ABCRabbitMQManager(ABC):
    @abstractmethod
    async def _create_connection(self) -> None: ...

    @abstractmethod
    async def _consume_messages(self) -> None: ...

    @abstractmethod
    async def close_connection(self) -> None: ...

    @abstractmethod
    async def _get_channel(self) -> None: ...

    @abstractmethod
    async def _create_connection_pool(self) -> None: ...

    @abstractmethod
    async def start(self) -> None: ...
