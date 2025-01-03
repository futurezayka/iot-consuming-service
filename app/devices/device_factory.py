from abc import ABC

from interfaces.device import Device


class DeviceFactory(ABC):
    @staticmethod
    def create_device() -> Device:
        raise NotImplementedError
