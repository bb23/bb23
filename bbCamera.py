#!/usr/bin/env python
import time

from picamera import PiCamera


class BbCamera(PiCamera):

    def __init__(self):
        PiCamera.__init__(self)
        self.hflip = self.vflip = True
        time.sleep(2)

