from uuid import UUID

from pydantic import BaseModel


class StreamCommand(BaseModel):
    type: str
    device_id: UUID
    device_type: str
