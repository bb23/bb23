#!/usr/bin/env python
import time

from picamera import PiCamera


class BbCamera(PiCamera):

    def __init__(self):
        super(PiCamera, self).__init__()
        self.hflip = self.vflip = True
        time.sleep(2)
