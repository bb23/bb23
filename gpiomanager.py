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
import yaml
import time
import logging
from threading import Thread

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

    def turn_left(self, seconds):
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


    def turn_right(self, seconds):
        print "Turning right."
        GPIO.output(rf_forward, LOW)
        GPIO.output(rf_backward, HIGH)

        GPIO.output(rr_forward, LOW)
        GPIO.output(rr_backward, HIGH)

        GPIO.output(lf_forward, LOW)
        GPIO.output(lf_backward, HIGH)

        GPIO.output(lr_forward, LOW)
        GPIO.output(lr_backward, HIGH)

        GPIO.output(rr_pwm, HIGH)
        GPIO.output(rf_pwm, HIGH)

        GPIO.output(lr_pwm, HIGH)
        GPIO.output(lf_pwm, HIGH)


    def forward(self, seconds):
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

    def stop(self, seconds):
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
        GPIO.cleanup()

# Scheduled command thread
class AsyncCmd(Thread):
    is_cancelled = False
    is_finished = False
    def __init__(self, timeout_sec, cmd, handle_cmd_cb, is_replaceable=True):
        # If is_replaceable is True and another timeout with the same command is added, the
        # existing timeout will be suspended and only the new one executed.
        Thread.__init__(self)
        self.timeout_sec = timeout_sec
        self.cmd = cmd
        self.handle_cmd_cb = handle_cmd_cb  # callback to execute command with
        self.is_replaceable = is_replaceable

    def run(self):
        time.sleep(self.timeout_sec)
        if not self.is_cancelled:
            self.handle_cmd_cb(self.cmd)
        self.is_finished = True


# Main GPIO handler class
class rGPIO(object):
    INPUT = GPIO.IN
    OUTPUT = GPIO.OUT
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW

    config = None
    commands = None
    async_pool = []

    def __init__(self, logger, configfile):
        self.logger = logger
        self.fn_config = configfile

        self.logger.info("Initializing gpio pins.")
        GPIO.setmode(GPIO_MODE)
        self._gpio_init()

        logger.info("Starting GPIODaemon...")
        self.driver = Driver(logger=logger)

        logger.info("Initialized driver")



    # Public Functions
    def setup(self, gpio_id, mode=OUTPUT):
        GPIO.setup(gpio_id, mode)

    def gpio_output(self, gpio_id, value=HIGH):
        GPIO.output(gpio_id, value)

    def gpio_readinput(self, gpio_id):
        return GPIO.input(gpio_id)

    def cleanup(self):
        # Reset all channels that have been set up
        GPIO.cleanup()

    def reload(self):
        self._gpio_init()

    def handle_cmd(self, cmd):
        # Called from tcp daemon if command comes in. Any return value will be sent
        # to the socket connection.
        cmd = cmd.strip()
        self.logger.info("cmd: '%s'" % cmd)

        if cmd == "reload":
            self.reload()

        elif cmd in self.commands:
            # translate user-command to system-command and execute
            return self._handle_cmd(self.commands[cmd])

        else:
            return self._handle_cmd(cmd)

    def _reload_config(self):
        self.config = yaml.load(open(self.fn_config))
        self.logger.info("Config loaded: %s", self.config)
        self.commands = self.config["commands"]

    def _gpio_init(self):
        # Read config and set modes accordingly
        GPIO.cleanup()
        self._reload_config()

        # Setup pins according to config file
        # for gpio_id, mode in self.config.get("gpio-setup").items():
        #     if mode == "OUTPUT":
        #         mode = self.OUTPUT
        #     elif mode == "INPUT":
        #         mode = self.INPUT
        #     else:
        #         self.logger.warn("Error: cannot set mode to '%s' (_gpio_init)", mode)
        #         return

        #     # Setup pin to default mode from config file
        #     self.setup(gpio_id, mode)

    def _handle_cmd(self, internal_cmd):
        # Internal cmd is the actual command (triggered by the user command).
        # Any return value will be sent to the socket connection.
        self.logger.info("execute> %s" % internal_cmd)
        cmd_parts = internal_cmd.split(" ")
        cmd = cmd_parts[0]

        if cmd == "set":
            gpio_id, value = cmd_parts[1:3]

            if value == "HIGH":
                value = self.HIGH

            elif value == "LOW":
                value = self.LOW

            else:
                self.logger.warn("Error cannot handle command '%s' due to bad value", internal_cmd)
                return

            self.gpio_output(int(gpio_id), value)

        elif cmd == "read":
            # examples:
            #   `read 17`  # reads the input on the gpio pin and returns the value
            gpio_id = cmd_parts[1]
            return self.gpio_readinput(gpio_id)

        elif cmd == "forward":
            self.logger.info("in command forward")
            self.driver.forward(1)
            return "going forward"

        elif cmd == "turn_left":
            self.logger.info("in command turn_left")
            self.driver.turn_left(1)
            return "turn left"

        elif cmd == "turn_right":
            self.logger.info("in command turn_right")
            self.driver.turn_right(1)
            return "turning_right"

        elif cmd == "stop":
            self.logger.info("in command stop")
            self.driver.stop(1)
            return "stop"

        elif cmd == "rtimeout":
            # Replaceable timeout. Replaces based on "cmd" only.
            timeout = cmd_parts[1]
            cmd = " ".join(cmd_parts[2:])
            self.logger.info("understood rtimeout. cmd in %s seconds: `%s`", timeout, cmd)

            # Disable all old ones from the pool
            for async_cmd in self.async_pool:
                if async_cmd.cmd == cmd and async_cmd.is_replaceable:
                    async_cmd.is_cancelled = True

            # Remove cancelled threads from the pool
            self.async_pool[:] = [t for t in self.async_pool if (not t.is_cancelled) and (not t.is_finished)]

            # Now add new task
            t = AsyncCmd(int(timeout), cmd, self.handle_cmd, is_replaceable=True)
            t.start()
            self.async_pool.append(t)

        else:
            self.logger.warn("command '%s' not recognized", cmd)


if __name__ == "__main__":
    # Setup Logging
    logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Run tests
    g = rGPIO(logger, "config.yaml")
    g.handle_cmd("thermo on")
    g.handle_cmd("rtimeout 3 thermo off")
    time.sleep(5)
    g.cleanup()
