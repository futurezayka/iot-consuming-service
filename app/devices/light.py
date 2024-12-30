import random
from datetime import datetime, timezone
import json
from interfaces.device import Device


class LightSensor(Device):
    async def retrieve_data(self):
        return json.dumps(
            {
                "telemetry": random.uniform(0, 100),
                "date": datetime.now(tz=timezone.utc).isoformat(),
            }
        )
