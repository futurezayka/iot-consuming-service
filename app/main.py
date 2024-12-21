import asyncio
import logging

from app.services.rabbitmq import rabbitmq_service

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    service = rabbitmq_service()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(service.start())
    loop.run_forever()
