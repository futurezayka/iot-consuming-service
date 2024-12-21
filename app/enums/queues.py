from enum import Enum


class Queues(Enum):
    command = "command_queue"
    data = "data:{device_id}:queue"
