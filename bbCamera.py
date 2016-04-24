#!/usr/bin/env python
from picamera import PiCamera


class bbCamera(PiCamera):

    def __init__(self):
        PiCamera.__init__(self)
        self.hflip = self.vflip = True


