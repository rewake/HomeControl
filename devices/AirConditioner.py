import platform
if platform.system() != 'pi':
    from gpiozero.pins.mock import MockFactory

from gpiozero import OutputDevice, BadPinFactory
print BadPinFactory.message
import logging


class AirConditioner(OutputDevice):
    """
    Air conditioner controller class
    """

    # Modes
    OFF = 0
    ON = 1
    AUTO = 2

    # Instantiate current mode as "OFF"
    mode = OFF

    def __init__(self, pin):
        super(OutputDevice, self).__init__(pin)

    def on(self):

        logging.debug("Turning AC On")
        super(AirConditioner, self).on()

    def off(self):

        logging.debug("Turning AC Off")
        super(AirConditioner, self).off()

    def auto(self):

        logging.debug("Turning AC Off")
        super(AirConditioner, self).off()

    def set_mode(self, mode=None):

        if mode is not None:

            logging.debug("Setting mode to: " + str(self.mode))
            self.mode = mode

        logging.debug("Current mode is: " + str(self.mode))
        return self.mode
