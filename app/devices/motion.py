import random
from datetime import datetime

from interfaces.device import Device


class MotionSensor(Device):
    async def retrieve_data(self):
        return {"telemetry": random.randint(0, 1), "date": datetime.now().isoformat()}
