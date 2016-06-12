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


# Do things that are related to the camera
class Camera(object):

    def __init__(self, logger):

        self.result = (-10, 10)
        logger.info("dummy gpio?")
        logger.info(is_dummy_gpio)

        # Initialize camera object

        print "Initialized Camera Object."

    def capture_image(self):
        print "Capturing image."

        # Capture image

    def get_result(self):
        print "Getting results"

        return self.result

    def analyze_image(self):
        print "Analyzing image"

        # Analyze image

    def cleanup(self):
        # clean up camera


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

    config = None
    commands = None
    async_pool = []

    def __init__(self, logger, configfile):
        self.logger = logger
        self.fn_config = configfile

        self.logger.info("Initializing camera.")
        # self._gpio_init()

        logger.info("Starting CameraDaemon...")
        self.camera = Camera(logger=logger)

        logger.info("Initialized camera")

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

    def _handle_cmd(self, internal_cmd):
        # Internal cmd is the actual command (triggered by the user command).
        # Any return value will be sent to the socket connection.
        self.logger.info("execute> %s" % internal_cmd)
        cmd_parts = internal_cmd.split(" ")
        cmd = cmd_parts[0]

        elif cmd == "get_results":
            self.logger.info("in command return results")
            return self.camera.get_results()

        elif cmd == "capture_image":
            self.logger.info("in command capture_image")
            self.camera.capture_image()
            return "capturing image"

        elif cmd == "analyze_image":
            self.logger.info("in command analyze_image")
            self.camera.analyze_image()
            return "turn left"

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
