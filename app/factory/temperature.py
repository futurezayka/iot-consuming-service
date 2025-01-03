from devices.device_factory import DeviceFactory
from devices.temperature import TemperatureSensor
from interfaces.device import Device


class TemperatureSensorFactory(DeviceFactory):
    @staticmethod
    def create_sensor() -> Device:
        return TemperatureSensor()
