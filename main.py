#!usr/bin/env python
import datetime
import logging
import random
from time import sleep
import socket
import subprocess
import os

PIDFILE = "/tmp/gpiodaemon.pid"

TICKLE = 0.2

TCP_IP = '127.0.0.1'
TCP_PORT = 9101
BUFFER_SIZE = 30


def send_command(command):
    logging.info("in send_command %s" % command)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(command + "\n")
    data = s.recv(BUFFER_SIZE)
    s.close()

    logging.info("received data: %s" % data)

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
    logging.basicConfig(filename='events.log', level=logging.DEBUG)
    try:
        os.system("python gpiodaemon.py start")
        logging.info("\n\nDriver enabled")

        camera_process = subprocess.Popen(['python', 'bbCamera.py'], shell=False)
        logging.info("\n\nCamera enabled")

        methods = ["forward", "turn_right", "turn_left"]
        loopery = True
        while loopery:

            with open("file_status.txt", 'r') as f:
                status = f.read().rstrip()

            if status == "no_ball":
                # Jitter'd random walk.
                print "==================================="
                print "     Random walk mode enabled      "
                print "==================================="
                random_method = random.choice(methods)
                send_command(random_method)
                sleep(TICKLE)
                continue

            elif status == "turn_left":
                send_command("turn_left")
            elif status == "turn_right":
                send_command("turn_right")
            else:
                send_command("forward")

    except Exception as e:
        error_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S.%f")
        import traceback
        logging.debug(error_timestamp + ": " + str(e))
        traceback.print_exc(file=open('traceback.log','a'))
    finally:
        logging.info("\n\nCleaning up")
        os.system("python gpiodaemon.py stop")
        os.system("python cleanup.py")
        camera_process.terminate()

if __name__ == "__main__":
    main()
