import random
from datetime import datetime

from interfaces.device import Device


class LightSensor(Device):
    async def retrieve_data(self):
        return {"telemetry": random.uniform(0, 100), "date": datetime.now().isoformat()}
