#!usr/bin/env python
import datetime
import logging
import random
from time import sleep
import socket

import cv2
import numpy as np
import picamera
import picamera.array
# from random_walker import RandomWalker

from bbCamera import BbCamera
import os
import sys
import signal
import socket
import logging
from optparse import OptionParser
from time import sleep

from tornado.ioloop import IOLoop
# from tornado.netutil import TCPServer
from tornado.tcpserver import TCPServer


LOGFILE = "gpiodaemon.log"
LOGLEVEL = logging.DEBUG

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.yaml")

PORT = 9101
PIDFILE = "/tmp/gpiodaemon.pid"


# Setup Logging
logging.basicConfig(filename=LOGFILE, format='%(levelname)s | %(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)


# Catch SIGINT to shut the daemon down (eg. via $ kill -s SIGINT [proc-id])
def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


# Each connected client gets a TCPConnection object
class TCPConnection(object):
    def __init__(self, gpio, stream, address):
        logger.debug('- new connection from %s' % repr(address))
        self.myGPIO = gpio
        self.stream = stream
        self.address = address
        self.stream.set_close_callback(self._on_close)
        self.stream.read_until('\n', self._on_read_line)

    def _on_read_line(self, data):
        data = data.strip()
        if not data or data == "quit":
            self.stream.close()
            return

        # Process input
        response = self.myGPIO.handle_cmd(data)
        logger.debug(response)
        if response:
            self.stream.write("%s\n" % response.strip())

        # Continue reading on this connection
        self.stream.read_until('\n', self._on_read_line)

    def _on_write_complete(self):
        pass

    def _on_close(self):
        logger.debug('- client quit %s' % repr(self.address))


# The main server class
class GPIOServer(TCPServer):
    def __init__(self, gpio, io_loop=None, ssl_options=None, **kwargs):
        self.myGPIO = gpio
        TCPServer.__init__(self, io_loop=io_loop, ssl_options=ssl_options, **kwargs)

    def handle_stream(self, stream, address):
        TCPConnection(self.myGPIO, stream, address)


# Helper to reload config of a running daemon
def daemon_reload():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", PORT))
        sock.sendall("reload\n\n")  # second newline (empty packet) terminates the connection server-side
    finally:
        sock.close()


class GPIODaemon(Daemon):
    def run(self):
        try:
            logger.info("Starting daemon")
            logger.info(dir(gpiomanager))
            myGPIO = gpiomanager.rGPIO(logger=logger, configfile=CONFIG_FILE)
            gpio_server = GPIOServer(myGPIO)
            gpio_server.listen(PORT)

            # Loop here
            IOLoop.instance().start()

        except SystemExit:
            logger.info("Shutting down via signal")

        except Exception as e:
            logger.exception(e)

        finally:
            try:
                myGPIO.cleanup()

            except Exception as e:
                logger.exception(e)

            finally:
                logger.info("GPIODaemon stopped")


PIDFILE = "/tmp/gpiodaemon.pid"

TICKLE = 0.2

LOWER = np.array([0, 70, 120])
UPPER = np.array([30, 160, 255])

VERBOTTEN_METHODS = set("cleanup")


TCP_IP = '127.0.0.1'
TCP_PORT = 9101
BUFFER_SIZE = 30


def send_command(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(command + "\n")
    data = s.recv(BUFFER_SIZE)
    s.close()

    print "received data:", data

"""
send_command("forward")
sleep(3)
send_command("turn_right")
sleep(3)
send_command("turn_left")
sleep(3)
send_command("stop")
"""


def main():
    logging.basicConfig(filename='/home/pi/bb23/example.log', level=logging.DEBUG)
    # start_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S.%f")
    # image_path = "/home/pi/bb23/images/%s_%s.jpg"
    try:
        cam = BbCamera()
        sleep(2)
        driver_daemon = GPIODaemon(PIDFILE)
        driver_daemon.start()

        # Initialize drive controller and get methods sans Verbotten

        logging.info("\n\nDriver enabled")

        methods = ["forward", "turn_right", "turn_left"]
        loopery = True
        while loopery:
            # CAPTURE IMAGE
            with picamera.array.PiRGBArray(cam) as stream:
                cam.capture(stream, 'bgr')
                image = stream.array

            # GRAB IMAGE ATTRIBUTES
            height, width, channels = image.shape
            # assign left right center region
            center_x_low = width / 2 - 100
            center_x_high = width / 2 + 100

            # BUILD COLOR MASK WITH CONSTANTS SET FOR ~ORANGE
            color_mask = cv2.inRange(image, LOWER, UPPER)

            # find contours in the masked image and keep the largest one
            (_, cnts, _) = cv2.findContours(color_mask.copy(),
                                            cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)

            if len(cnts) == 0:
                # Jitter'd random walk.
                print "==================================="
                print "     Random walk mode enabled      "
                print "==================================="
                random_method = random.choice(methods)
                send_command(random_method)
                sleep(TICKLE)
                continue

            c = max(cnts, key=cv2.contourArea)

            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.05 * peri, True)

            M = cv2.moments(approx)
            try:
                c_x = int(M['m10']/M['m00'])
                # c_y = int(M['m01']/M['m00'])
            except ZeroDivisionError:
                logging.info("dividing by zero")
                continue

            if c_x < center_x_low:
                send_command("turn_left")
                sleep(TICKLE/2)
                # drive_controller.right_motor_high_forward(TICKLE/2)
            elif c_x > center_x_high:
                send_command("turn_right")
                sleep(TICKLE/2)
                # drive_controller.left_motor_high_forward(TICKLE/2)
            else:
                send_command("forward")
                sleep(TICKLE/2)
                # drive_controller.forward(TICKLE/2)

    except Exception as e:
        error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S.%f")
        import traceback
        logging.debug(error_timestamp + ": " + str(e))
        logging.debug(traceback.print_exc(file=open('/home/pi/bb23/traceback.log','a')))

if __name__ == "__main__":
    main()
