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


# Right front motor
rf_forward = 18
rf_backward = 16
rf_pwm = 12

#Right Rear Motor
rr_forward = 33
rr_backward = 31
rr_pwm = 29

# Left front motor
lf_forward = 15
lf_backward = 13
lf_pwm = 11

#left Rear Motor
lr_forward = 36
lr_backward = 37
lr_pwm = 32

HIGH = GPIO.HIGH
LOW = GPIO.LOW
OUT = GPIO.OUT

# BCM Mode uses GPIO ids, BOARD Mode uses pin ids
# GPIO_MODE = GPIO.BCM
GPIO_MODE = GPIO.BOARD


class Driver(object):

    def __init__(self, logger):
        logger.info("dummy gpio?")
        logger.info(is_dummy_gpio)

        logger.info(dir(GPIO))
        logger.info(GPIO.__class__)
        # Initialize Right Front Motor
        GPIO.setup(rf_forward, OUT)
        GPIO.setup(rf_backward, OUT)
        GPIO.setup(rf_pwm, OUT)

        # Initialize Left Front Motor
        GPIO.setup(lf_forward, OUT)
        GPIO.setup(lf_backward, OUT)
        GPIO.setup(lf_pwm, OUT)

        # Initialize Right Rear Motor
        GPIO.setup(rr_forward, OUT)
        GPIO.setup(rr_backward, OUT)
        GPIO.setup(rr_pwm, OUT)

        # Initialize Left Rear Motor
        GPIO.setup(lr_forward, OUT)
        GPIO.setup(lr_backward, OUT)
        GPIO.setup(lr_pwm, OUT)

        print "Initialized Driver Object."

    def turn_left(self):
        print "Turning left."
        GPIO.output(rf_forward, HIGH)
        GPIO.output(rf_backward, LOW)

        GPIO.output(rr_forward, HIGH)
        GPIO.output(rr_backward, LOW)

        GPIO.output(lf_forward, LOW)
        GPIO.output(lf_backward, HIGH)

        GPIO.output(lr_forward, LOW)
        GPIO.output(lr_backward, HIGH)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(rf_pwm, HIGH)

        GPIO.output(lr_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)


    def turn_right(self):
        print "Turning right."
        GPIO.output(rf_forward, LOW)
        GPIO.output(rf_backward, HIGH)

        GPIO.output(rr_forward, LOW)
        GPIO.output(rr_backward, HIGH)

        GPIO.output(lf_forward, HIGH)
        GPIO.output(lf_backward, LOW)

        GPIO.output(lr_forward, HIGH)
        GPIO.output(lr_backward, LOW)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(rf_pwm, HIGH)

        GPIO.output(lr_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)


    def forward(self):
        print "Forward engaged."
        # forward pins to high
        GPIO.output(rf_forward, HIGH)
        GPIO.output(rr_forward, HIGH)

        GPIO.output(lf_forward, HIGH)
        GPIO.output(lr_forward, HIGH)

        # back pins to low
        GPIO.output(rf_backward, LOW)
        GPIO.output(rr_backward, LOW)

        GPIO.output(lf_backward, LOW)
        GPIO.output(lr_backward, LOW)

        # engage pwmm
        GPIO.output(rf_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(lr_pwm, HIGH)

    def stop(self):
        print("Stopping")

        GPIO.output(rf_forward, LOW)
        GPIO.output(rr_forward, LOW)

        GPIO.output(lf_forward, LOW)
        GPIO.output(lr_forward, LOW)

        # back pins to low
        GPIO.output(rf_backward, LOW)
        GPIO.output(rr_backward, LOW)

        GPIO.output(lf_backward, LOW)
        GPIO.output(lr_backward, LOW)

        # engage pwmm
        GPIO.output(rf_pwm, LOW)
        GPIO.output(lf_pwm, LOW)

        GPIO.output(rr_pwm, LOW)
        GPIO.output(lr_pwm, LOW)


    def cleanup(self):
        self.stop()
        GPIO.cleanup()


# Main GPIO handler class
class rGPIO(object):

    def __init__(self, logger):
        self.logger = logger

        self.logger.info("Initializing gpio pins.")
        GPIO.setmode(GPIO_MODE)
        self._gpio_init()

        logger.info("Starting GPIODaemon...")
        self.driver = Driver(logger=logger)

        logger.info("Initialized driver")


    def cleanup(self):
        # Reset all channels that have been set up
        GPIO.cleanup()


    def handle_cmd(self, cmd):
        # New handle command class that's simpler

        cmd = cmd.strip()
        self.logger.info("cmd: '%s'" % cmd)

        return self._handle_cmd(cmd)


    def _gpio_init(self):
        # Read config and set modes accordingly
        GPIO.cleanup()

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

        else:
            self.logger.warn("command '%s' not recognized", cmd)


if __name__ == "__main__":
    # Setup Logging
    logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Run tests
    g = rGPIO(logger)
    g.handle_cmd("forward")
    g.handle_cmd("turng_left")
    time.sleep(5)
    g.cleanup()
