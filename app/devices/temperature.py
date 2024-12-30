import random
from datetime import datetime, timezone
import json
from interfaces.device import Device


class TemperatureSensor(Device):
    async def retrieve_data(self):
        return json.dumps(
            {
                "telemetry": random.uniform(0, 25),
                "date": datetime.now(tz=timezone.utc).isoformat(),
            }
        )
