import random
from datetime import datetime

from interfaces.device import Device


class TemperatureSensor(Device):
    async def retrieve_data(self):
        return {"telemetry": random.uniform(0, 25), "date": datetime.now().isoformat()}
