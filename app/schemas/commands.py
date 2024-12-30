from pydantic import BaseModel


class StreamCommand(BaseModel):
    type: str
    device_id: str
    device_type: str
