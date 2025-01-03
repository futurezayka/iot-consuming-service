from devices.device_factory import DeviceFactory
from devices.light import LightSensor
from interfaces.device import Device


class LightSensorFactory(DeviceFactory):
    @staticmethod
    def create_sensor() -> Device:
        return LightSensor()
