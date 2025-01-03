from devices.device_factory import DeviceFactory
from devices.motion import MotionSensor
from interfaces.device import Device


class MotionSensorFactory(DeviceFactory):
    @staticmethod
    def create_sensor() -> Device:
        return MotionSensor()
