#!/usr/bin/env python
from picamera import PiCamera


class bbCamera(PiCamera):

    def __init__(self):
        super(PiCamera, self).__init__()
        self.hflip = self.vflip = True
