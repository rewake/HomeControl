import platform
if platform.system() != 'pi':
    from gpiozero.pins.mock import MockFactory

from gpiozero import OutputDevice, BadPinFactory
print BadPinFactory.message
import logging


class AirConditioner():
    """
    Air conditioner controller class
    """

    # Constants
    OFF = 0
    ON = 1
    AUTO = 2

    def __init__(self, pin):
        super(OutputDevice, self).__init__(pin)

    def on(self):

        logging.debug("Turning AC On")
        super(AirConditioner, self).on()

    def off(self):

        logging.debug("Turning AC Off")
        super(AirConditioner, self).off()
