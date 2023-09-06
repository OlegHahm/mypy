#!/usr/bin/python3

import logging

class TestLogger:

    def __init__(self):
        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)

    def test_f(self):
        print("Level: %s" % self.logger.getEffectiveLevel())
        self.logger.log(logging.DEBUG, "debug")
        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warning")
        self.logger.error("error")

tl = TestLogger()
tl.test_f()
