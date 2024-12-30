import random
from datetime import datetime, timezone
import json
from interfaces.device import Device


class MotionSensor(Device):
    async def retrieve_data(self):
        return json.dumps(
            {
                "telemetry": random.randint(0, 1),
                "date": datetime.now(tz=timezone.utc).isoformat(),
            }
        )
