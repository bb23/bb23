"""
Receives user-commands and communicates with the RPi.GPIO lib to switch the
pins etc. Also manages scheduled tasks (eg. "rtimeout 1800 thermo off" to
execute the command "thermo off" in 30 minutes (1800 seconds).

Use:

    GPIO = gpiomanager.GPIO("settings.yaml")
    GPIO.setup(17, GPIO.OUTPUT)
    GPIO.gpio_output(17, GPIO.HIGH)
    value = gpio_readinput(17)

    GPIO.cleanup()

    GPIO.reload()
    GPIO.handle_cmd(<cmd>)
"""
import time
import logging

from driver import Driver

# Import GPIO module -- either the dummy or the real lib
try:
    import RPi.GPIO as GPIO
    is_dummy_gpio = False

except ImportError:
    import dummy
    GPIO = dummy.Dummy()
    is_dummy_gpio = True

except:
    # Will alert user if not run as root.
    raise


# Main GPIO handler class
class rGPIO(object):

    def __init__(self, logger):
        self.logger = logger

        logger.info("Starting GPIODaemon...")
        self.driver = Driver(logger=logger)

        logger.info("Initialized driver")

    def handle_cmd(self, cmd):
        # New handle command class that's simpler

        cmd = cmd.strip()
        self.logger.info("cmd: '%s'" % cmd)

        return self._handle_cmd(cmd)

    def _handle_cmd(self, internal_cmd):
        # Internal cmd is the actual command (triggered by the user command).
        # Any return value will be sent to the socket connection.
        self.logger.info("execute> %s" % internal_cmd)
        cmd_parts = internal_cmd.split(" ")
        cmd = cmd_parts[0]

        if cmd == "forward":
            self.logger.info("in command forward")
            self.driver.forward()
            return "going forward"

        elif cmd == "turn_left":
            self.logger.info("in command turn_left")
            self.driver.turn_left()
            return "turn left"

        elif cmd == "turn_right":
            self.logger.info("in command turn_right")
            self.driver.turn_right()
            return "turning_right"

        elif cmd == "stop":
            self.logger.info("in command stop")
            self.driver.stop()
            return "stop"

        elif cmd == "backward":
            self.logger.info("in command backward")
            self.driver.backward()
            return "backwards"

        else:
            self.logger.warn("command '%s' not recognized", cmd)


if __name__ == "__main__":
    # Setup Logging
    logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Run tests
    g = rGPIO(logger)
    g.handle_cmd("forward")
    g.handle_cmd("turn_left")
    time.sleep(5)
    g.cleanup()
