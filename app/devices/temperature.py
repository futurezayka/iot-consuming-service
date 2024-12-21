import random

from interfaces.device import Device


class TemperatureSensor(Device):
    async def retrieve_data(self):
        return {"value": random.uniform(0, 25), "unit": "C"}
