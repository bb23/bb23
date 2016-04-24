#!/usr/bin/env python
import inspect
import random
import time

from driver import Driver

VERBOTTEN_METHODS = set("cleanup")


class RandomWalker(object):

    def __init__(self):
        self.driver = Driver()

    def walk_by_time(self, length_of_time):
        now = time.time()
        length_in_ms = length_of_time*1000
        then = now + length_in_ms
        while time.time() < then:
            remaining_time = (time.time() - then) / 1000
            random_seconds = random.randint(1, remaining_time)
            self.random_method(random_seconds)
        self.driver.cleanup()

    def random_method(self, time):
        methods = set(inspect.getmembers(self.driver, predicate=inspect.ismethod))
        methods -= VERBOTTEN_METHODS
        random_method = random.choice(methods)
        getattr(self.driver, random_method(time))
