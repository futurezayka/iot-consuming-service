import asyncio
import logging

from managers.rabbitmq import get_rabbitmq_manager

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = get_rabbitmq_manager()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(service.start())
    loop.run_forever()
