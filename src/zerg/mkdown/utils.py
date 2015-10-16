# -*- coding: utf-8 -*-
import os
import logging
import sys


def pathjoin(*args):
    cp = os.path.dirname(__file__)
    return os.path.join(cp, *args)


LOGGER_NAME = 'saika.mkdwon'
LOGGER_LEVEL = logging.DEBUG
# LOGGER_FORMATTER = '[%(name)s] %(message)s'
LOGGER_FORMATTER = '%(message)s'

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(LOGGER_LEVEL)
formatter = logging.Formatter(LOGGER_FORMATTER)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

# Accept title level not great than RECUR_DEEP
# If title level great than RECUR_DEEP, Handle as RECUR_DEEP levels
# RECUR_DEEP could only in (2, 3)
RECUR_DEEP = 3

assert RECUR_DEEP in (2, 3)


class Error(Exception):
    pass